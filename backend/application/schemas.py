from pydantic import BaseModel, Field


class TaskStatusSchema(BaseModel):
    id: str
    status: str
