from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import cats_markup, numbers


@dp.message_handler(state=ShopState.amount)
async def get_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    product_name = data.get("product_name")
    product_price = data.get("product_price")
    cart_id = data.get("cart_id")
    amount = message.text
    if int(amount) > 0:
        amount = int(amount)
        db.add_cart_item(product_id=product_id, quantity=amount, cart_id=cart_id)
        await message.answer(f"<b>{product_name}</b>\n\n<code>{product_name} x {amount} = {product_price * amount} so'm</code>\n\n<i>Xo'sh davom etamizmi 😍?</i>", parse_mode="html", reply_markup=cats_markup)
        await ShopState.category.set()
    else:
        await message.answer("Miqdorni to'g'ri raqamlar bilan kiriting ☺️", reply_markup=numbers)