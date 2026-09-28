from pydantic import BaseModel
from typing import List, Optional


class Task(BaseModel):
    id: int
    title: str
    priority: str
    deadline: Optional[str] = None
    status: str = "pending"


class DigitalTwin(BaseModel):
    name: str
    goals: List[str]
    preferences: List[str]
    tasks: List[Task]