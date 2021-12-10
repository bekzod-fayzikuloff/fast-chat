from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.responses import Response

from .. import schemas
from ..services.chats import ChatService
from ..schemas.chats import Chat

router = APIRouter(prefix="/chats")


@router.get("/", response_model=List[Chat])
def chats_list(chat_service: ChatService = Depends()):
    return chat_service.get_many()


@router.post("/", response_model=Chat, status_code=status.HTTP_201_CREATED)
def create_chat(chat_data: schemas.ChatCreate, chat_service: ChatService = Depends()):
    return chat_service.create(chat_data)


@router.get("/{chat_id}", response_model=schemas.Chat)
def get_chat(chat_id: int, chat_service: ChatService = Depends()):
    return chat_service.get(chat_id=chat_id)


@router.put("/{chat_id}", response_model=schemas.Chat)
def update_chat(chat_id: int, chat_data: schemas.ChatUpdate, chat_service: ChatService = Depends()):
    return chat_service.update(chat_id=chat_id, chat_data=chat_data)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, chat_service: ChatService = Depends()):
    chat_service.delete(chat_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
