import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()

# MongoDB configuration
MONGO_URI = "mongodb://mongo:27017/"
DATABASE_NAME = "mqtt_data"
COLLECTION_NAME = "payload"

# MongoDB client and collection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.get("/mqtt-payloads")
async def get_mqtt_payloads():
    try:
        # Fetch all records from the collection
        payloads = collection.find()
        payload_list = []

        # iterate through the payloads and add them to the list
        for payload in payloads:
            payload_list.append({
                "session_id": payload.get("session_id"),
                "energy_delivered_in_kWh": payload.get("energy_delivered_in_kWh"),
                "duration_in_seconds": payload.get("duration_in_seconds"),
                "session_cost_in_cents": payload.get("session_cost_in_cents"),
            })

        return payload_list

    except Exception as e:
        # Log the error using the logger
        logger.error(f"Error: {e}")
        # Return an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(status_code=500, detail="Internal Server Error")
