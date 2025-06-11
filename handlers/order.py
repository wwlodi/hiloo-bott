from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states.order_state import OrderStates
from keyboards.category import choose_category_kb
from keyboards.products import build_products_kb
from keyboards.quantity import quantity_back_kb
from keyboards.new_order import new_order_kb
from data.products import STICKS, CIGARETTES
from config import settings

router = Router()

@router.callback_query(F.data == "order_start")
async def order_start(callback: CallbackQuery):
    try:
        # Якщо є текст — редагуємо
        if callback.message.text:
            await callback.message.edit_text(
                "Выберите категорию товара:",
                reply_markup=choose_category_kb()
            )
        else:
            # fallback якщо це було фото або щось інше
            await callback.message.answer(
                "Выберите категорию товара:",
                reply_markup=choose_category_kb()
            )
    except Exception as e:
        await callback.message.answer(
            "⚠️ Ошибка при возврате в меню.",
        )
    await callback.answer()



@router.callback_query(F.data == "category_sticks")
async def sticks_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите стики:",
        reply_markup=build_products_kb(STICKS, "sticks")
    )
    await callback.answer()


@router.callback_query(F.data == "category_cigs")
async def cigs_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите сигареты:",
        reply_markup=build_products_kb(CIGARETTES, "cigs")
    )
    await callback.answer()

@router.callback_query(F.data.startswith("product:"))
async def product_selected(callback: CallbackQuery, state: FSMContext):
    _, category, product_name = callback.data.split(":", 2)

    from data.products import STICKS, CIGARETTES
    products = STICKS if category == "sticks" else CIGARETTES
    price = products[product_name]

    await state.update_data(product=product_name, price=price)

    await callback.message.edit_text(
        f"Вы выбрали: <b>{product_name}</b> за <b>{price}€</b>.\n\n"
        "Введите количество пачек:",
        reply_markup=quantity_back_kb()
    )

    await state.set_state(OrderStates.waiting_for_quantity)
    await callback.answer()


@router.callback_query(F.data == "quantity_back")
async def back_to_products(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = data.get("product")

    from data.products import STICKS, CIGARETTES
    if product in STICKS:
        category = "sticks"
        products = STICKS
    elif product in CIGARETTES:
        category = "cigs"
        products = CIGARETTES
    else:
        await callback.message.answer("❗ Произошла ошибка при возврате.")
        return

    await callback.message.edit_text(
        "Выберите товар заново:",
        reply_markup=build_products_kb(products, category)
    )
    await callback.answer()
    await state.clear()  # очищаємо FSM, щоб почати знову

@router.callback_query(F.data == "new_order")
async def new_order(callback: CallbackQuery):
    await callback.message.answer(
        "Выберите категорию товара:",
        reply_markup=choose_category_kb()
    )
    await callback.answer()


@router.message(OrderStates.waiting_for_quantity)
async def get_quantity(message: Message, state: FSMContext, bot: Bot):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите число.")
        return

    count = int(message.text)
    data = await state.get_data()
    product = data["product"]
    price = data["price"]
    total = price * count

    await message.answer(
        f"✅ Спасибо за заказ! В ближайшее время с вами свяжется менеджер.\n\n"
        
        "📗 Детали заказа: \n\n"
        f"<b>{product}</b>\n"
        f"Кол-во: {count} шт\n"
        f"Сумма: <b>{total}€</b>\n\n"
        f"HiLo ❤️\n"
        f"Чтобы быть в курсе новинок — заходите в чат: https://t.me/+JU9k897lp282MmI0",
        reply_markup=new_order_kb()
    )


    user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    await bot.send_message(
        chat_id=settings.ADMIN_CHANNEL_ID,
        text=(
            f"📥 Новый заказ:\n"
            f"Покупатель: {user_tag}\n"
            f"Товар: {product}\n"
            f"Количество: {count} шт\n"
            f"Сумма: {total}€\n\n"
            "@hilo_manager"
        )
    )

    await state.clear()