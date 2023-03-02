import asyncio
import os
from fastapi import Body, FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import parse_obj_as
from typing import List

from .worker import celery, fetch_data
from .schemas import TaskStatusSchema
from .models import FlightModel


import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
)
db = client.flights
collection = db.flights

collection.create_index("hex", unique=True)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# bottleneck, sync code with IO bound, can be refactored to threads/async
def active_task_id() -> str | None:
    task_id = None
    if not (inspected := celery.control.inspect().active()):
        return task_id

    for _, tasks in inspected.items():
        for task in tasks:
            # magic constant here :)
            if task.get("name", None) == "fetch_data":
                task_id = task["id"]
                break
        else:
            continue
        break

    return task_id


@app.get("/task")
def get_task(task_id: str = None) -> TaskStatusSchema | None:
    if not task_id:
        task_id = active_task_id()

    if not task_id:
        return None

    # bottleneck, sync code with IO bound, can be refactored to threads/async
    task_result = celery.AsyncResult(task_id)

    return TaskStatusSchema(id=task_id, status=task_result.status)


@app.post("/task", status_code=201)
def run_task() -> str | None:
    if active_task_id():
        # or maybe return active task_id here instead of None?
        return None

    task = fetch_data.delay()
    return task.id


@app.get("/flights")
async def get_flights() -> List[FlightModel]:
    return parse_obj_as(List[FlightModel], await collection.find().to_list(1000))
