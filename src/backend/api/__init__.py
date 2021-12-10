from fastapi import APIRouter

from .chats import router as chats_router
from .messages import router as messages_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(chats_router)
router.include_router(messages_router)
router.include_router(auth_router)
