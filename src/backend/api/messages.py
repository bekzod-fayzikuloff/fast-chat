from fastapi import APIRouter, Depends

from ..services.messages import MessageService

router = APIRouter(
    prefix="/messages",
)


@router.get("/{chat_id}")
def chat_messages(chat_id: int, message_service: MessageService = Depends()):
    return message_service.get_message(chat_id)
