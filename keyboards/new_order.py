from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def new_order_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новый заказ", callback_data="new_order")]
    ])