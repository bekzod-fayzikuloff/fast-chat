from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel


class BaseChat(BaseModel):
    name: str
    description: Optional[str]
    created_at: datetime


class ChatCreate(BaseChat):
    pass


class ChatUpdate(BaseChat):
    pass


class Chat(BaseChat):
    id: int

    class Config:
        orm_mode = True
