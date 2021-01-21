from fastapi import APIRouter, Depends, Request
import json
import requests
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.database.database import get_db
from app.database.models import User
from app.telegram.handlers import MessageHandler, reply_unknown_user
from app.telegram.models import Chat


router = APIRouter(
    prefix="/telegram",
    tags=["telegram"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def telegram(request: Request, session=Depends(get_db)):

    # todo: Add templating
    return "Start using PyLander telegram bot!"


@router.post("/")
async def bot_client(request: Request, session=Depends(get_db)):
    req = await request.json()
    chat = Chat(req)
    message = MessageHandler(chat)

    # Check if current chatter in DB
    user = session.query(User).filter_by(telegram_id=chat.user_id).first()

    if user is None:
        return await reply_unknown_user(chat)
    else:
        # Process reply
        message.process_callback()
        return user
