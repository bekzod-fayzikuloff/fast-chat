from datetime import datetime
from pydantic import BaseModel


class BaseMassage(BaseModel):
    text: str
    created_at: datetime


class MessageCreate(BaseMassage):
    pass


class MessageUpdate(BaseMassage):
    pass


class Message(BaseMassage):
    id: int

    class Config:
        orm_mode = True
