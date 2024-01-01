import paho.mqtt.client as mqtt
import json
import pymongo



mongodb_url = "mongodb://mongo:27017/"


def getDBClient():
    client = pymongo.MongoClient(mongodb_url)
    return client["mqtt_data"]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("charger/1/connector/1/session/1")  # Subscribe to the same channel
    else:
        print(f"Connection failed with result code {rc}")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    db = getDBClient()
    payload_collection = db["payload"]
    payload_collection.insert_one(payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-broker", 1883, 60)

# Start the MQTT client loop to handle incoming messages
client.loop_start()

try:
    while True:
        # Add any additional processing or logic here
        pass
except KeyboardInterrupt:
    print("Application terminated by user")
finally:
    # Stop the MQTT client loop on application exit
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker")
