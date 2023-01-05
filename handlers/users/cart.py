from aiogram import types
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(text="Savatcha 🛒", state="*")
async def get_cart_items(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    items = db.get_all_items(cart_id=cart_id)
    msg = "«❌ Taom » - taomni savatdan o'chirish\n«🗑 Bo'shatish » - savatni bo'shatadi\n\nSavatdagi mahsulotlar:\n\n"
    total_price = 0
    for item in items:
        data = db.get_product_data(id=item[0])
        price = data[-2] * item[1]
        msg += f"{data[1]}\n{data[-2]} x {item[1]} = {price} so'm\n"
        total_price += price
    msg += f"\n\nUmumiy hisob: {total_price} so'm"  
    await message.answer(msg)  