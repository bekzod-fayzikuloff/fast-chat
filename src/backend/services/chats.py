from typing import List, Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from .. import tables
from .. import schemas
from ..database import get_session


class ChatService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self) -> List[tables.Chat]:
        chats = self.session.query(tables.Chat).all()
        return chats

    def get(self, chat_id):
        return self._get(chat_id=chat_id)

    def create(self, chat_data: schemas.ChatCreate) -> tables.Chat:
        chat = tables.Chat(**chat_data.dict())
        self.session.add(chat)
        self.session.commit()
        return chat

    def update(self, chat_id: int, chat_data: schemas.ChatUpdate) -> Optional[tables.Chat]:
        chat = self._get(chat_id=chat_id)
        for field, value in chat_data:
            setattr(chat, field, value)
        self.session.commit()
        return chat

    def delete(self, chat_id: int):
        chat = self._get(chat_id=chat_id)
        self.session.delete(chat)
        self.session.commit()

    def _get(self, chat_id: int) -> Optional[tables.Chat]:
        chat = (
            self.session.query(tables.Chat)
            .filter(
                tables.Chat.id == chat_id,
            )
            .first()
        )
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return chat
