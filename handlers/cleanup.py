from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("clear"))
async def clear_bot_messages(message: Message, bot):
    chat_id = message.chat.id
    deleted = 0

    try:
        async for msg in bot.iter_history(chat_id, limit=50):
            if msg.from_user and msg.from_user.id == (await bot.me()).id:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
                    deleted += 1
                    if deleted >= 10:
                        break
                except Exception:
                    continue
        await message.answer(f"🧹 Удалено сообщений: {deleted}")
    except Exception as e:
        await message.answer("❗ Ошибка при очистке чата.")
