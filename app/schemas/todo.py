from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=1000)

class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length =30)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)