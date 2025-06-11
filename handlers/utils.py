from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("get_chat_id"))
async def get_chat_id(message: Message):
    await message.answer(f"<b>Chat ID:</b> <code>{message.chat.id}</code>")
