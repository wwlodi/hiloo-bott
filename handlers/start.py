from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from keyboards.main_menu import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    image = FSInputFile("assets/logo.jpg")
    await message.answer_photo(
        photo=image,
        caption="Добро пожаловать в <b>HiLo</b>!\n\nНажмите кнопку ниже чтобы сделать заказ:",
        reply_markup=get_main_menu()
    )

