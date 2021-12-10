from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import get_session


class MessageService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_message(self, chat_id: int):
        pass
