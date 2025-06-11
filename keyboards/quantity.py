from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def quantity_back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="quantity_back")]
    ])
