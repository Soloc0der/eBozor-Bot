from aiogram import types
from states.main import ShopState
from loader import dp, db
import asyncio
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
    username = message.from_user.first_name
    await message.reply("bu bo'lim tez orada qo'shiladi 🤩")
    await message.answer(f"{username}, kechirasiz, xali bu bolim ishga tushmadi 😔")

@dp.message_handler(text="Hamyonim 💰", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    username = message.from_user.first_name
    await message.reply("bu bo'lim tez orada qo'shiladi 🤩")
    await message.answer(f"{username}, kechirasiz, xali bu bo'lim ishga tushmadi 😔")



@dp.message_handler(text="/love", state="*")
async def bot_echo(message: types.Message):
    username = message.from_user.first_name
    cnt = 0
    while cnt <= 500:
        await message.answer(f"{cnt} I love You - {username}♥️")
        cnt +=1
        await asyncio.sleep(0.05)

