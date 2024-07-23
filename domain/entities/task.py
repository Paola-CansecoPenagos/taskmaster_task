from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime, date, time

class Subtask(BaseModel):
    title: str = Field(...)
    completed: bool = Field(False) 

class Task(BaseModel):
    user_id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    category: str = Field(...)
    priority: str = Field(...)
    start_reminder_date: datetime = Field(...) 
    due_date: datetime = Field(...)            
    due_time: str = Field(...)            
    start_reminder_time: str = Field(...)  
    end_reminder_time: str = Field(...)
    subtasks: List[Subtask] = Field(default_factory=list)
    type: str = Field(...)
    progress: int = Field(0)