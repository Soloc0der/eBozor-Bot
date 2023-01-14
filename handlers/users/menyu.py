from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import cats_markup



@dp.message_handler(text="PHONE 📱", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    await state.update_data({"cart_id": cart_id})
    await message.answer("<b>O'zingizga kerakli bo'limni tanlang</b> 🌐\n\nSizni qaysi turdagi telefon qiziqtiryabdi? 🧐", reply_markup=cats_markup)
    await ShopState.category.set()



@dp.message_handler(text="Sozlamalar ⚙️", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(text="Hamyonim 💰", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    pass



