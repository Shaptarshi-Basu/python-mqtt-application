import paho.mqtt.client as mqtt
import json
import time
import random

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with result code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message Published with MID: {mid}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("mqtt-broker", 1883, 60)

while True:
    try:
        if not client.is_connected():
            print("Reconnecting to MQTT broker...")
            client.reconnect()

        energy = random.randint(0, 100)
        duration = random.randint(0, 60)
        session_cost = random.randint(1, 300)

        payload = {
            "session_id": 1,
            "energy_delivered_in_kWh": energy,
            "duration_in_seconds": duration,
            "session_cost_in_cents": session_cost
        }

        result = client.publish("charger/1/connector/1/session/1", json.dumps(payload), qos=1)
        client.loop()

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("Success: Message Published")
        else:
            print(f"Error: Failed to publish message. Result Code: {result.rc}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(60)  # Sleep for 1 second before the next iteration
