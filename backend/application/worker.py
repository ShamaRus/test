import os
from datetime import datetime
import json
from bson.objectid import ObjectId
import requests
from pymongo.errors import DuplicateKeyError
import pymongo

from celery import Celery

from .models import FlightModel

client = pymongo.MongoClient(os.environ.get("MONGODB_URL", "mongodb://localhost:27017"))
db = client.flights
collection = db.flights


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="fetch_data")
def fetch_data():
    API_KEY = os.environ.get("API_KEY", None)
    if not API_KEY:
        return

    now = datetime.now()

    response = requests.get(
        os.environ.get("API_ENDPOINT", "https://airlabs.co/api/v9/flights"),
        params={
            "api_key": API_KEY,
            "dep_iata": os.environ.get("API_DEP_IATA", "BER"),
        },
    )

    if response.status_code != 200:
        return

    result = response.json()

    # result = json.load(open(os.path.join(os.path.dirname(__file__), "data.json"), "r"))

    try:
        data = result["response"]
    except KeyError:
        return
    for flight_raw in data:
        flight = FlightModel.parse_obj(flight_raw)
        try:
            collection.insert_one(flight.dict())
        except DuplicateKeyError:
            exists = collection.find_one({"hex": flight.hex})
            collection.update_one(
                {"_id": ObjectId(exists["_id"])}, {"$set": flight.dict()}
            )

    # need to cleanup landed flights here

    collection.delete_many({"parsed": {"$lt": now}})
    collection.delete_many({"status": {"$ne": "en-route"}})
