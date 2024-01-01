import paho.mqtt.client as mqtt
import json
import pymongo
import logging

logging.basicConfig(level=logging.INFO)

mongodb_url = "mongodb://mongo:27017/"

def getDBClient():
    client = pymongo.MongoClient(mongodb_url)
    return client["mqtt_data"]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe("charger/1/connector/1/session/1")
    else:
        logging.error(f"Connection failed with result code {rc}")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    db = getDBClient()
    payload_collection = db["payload"]
    payload_collection.insert_one(payload)
    logging.info("Message received and inserted into the database")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-broker", 1883, 60)

# Start the MQTT client loop to handle incoming messages
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    logging.info("Application terminated by user")
finally:
    # Stop the MQTT client loop on application exit
    client.loop_stop()
    client.disconnect()
    logging.info("Disconnected from MQTT broker")
