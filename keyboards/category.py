from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def choose_category_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Стики", callback_data="category_sticks")],
        [InlineKeyboardButton(text="🚬 Сигареты", callback_data="category_cigs")]
    ])