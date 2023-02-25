from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import back_btn, cart_btn
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



@dp.message_handler(text="PHONE 📱", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    # await state.finish()   
    cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cats_markup.add(back_btn, cart_btn)
    cats = db.select_all_cats()
    for cat in cats:
        cats_markup.insert(KeyboardButton(text=cat[1]))



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


