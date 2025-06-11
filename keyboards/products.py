from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_products_kb(products: dict, category: str) -> InlineKeyboardMarkup:
    keyboard = []
    for name, price in products.items():
        callback_data = f"product:{category}:{name}"
        keyboard.append([InlineKeyboardButton(text=f"{name} - {price}€", callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="order_start")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
