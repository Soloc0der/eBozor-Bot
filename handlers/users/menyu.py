from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



@dp.message_handler(text="PHONE 📱", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    await state.finish()   
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
    try:
        username = message.from_user.username
        id = message.from_user.id
        db.sozlamalar_username(username=username, id=id)
    except:
        print("unable to update username")



    











@dp.message_handler(text="Sozlamalar ⚙️", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    malumot = db.select_profile(id=message.from_user.id)
    print(malumot)
    name = malumot[1]
    username = malumot[2]
    photo = malumot[3]

    if photo == None:
        photo = "AgACAgIAAxkBAAInUGQqYtru_HaRgXIO4BIf8-lzUtuNAAIYyDEb8ytQSQwqIL_q0ZgsAQADAgADcwADLwQ"
    phone = malumot[4]
    if phone == None:
        phone = "Kiritilmagan!"
    loc = malumot[5]
    if loc == None:
        loc = "Kiritilmagan!"

    msg = f"Sizning <b>Profil</b>ingiz ! \n\nIsm: {name} 👤\nUsername: @{username} 📨\n\nTelefon Raqam: +{phone} ☎️\nJoylashuv: {loc} 🏙"
    await message.answer_photo(photo=photo, caption=msg, reply_markup=sozlamalar)
    await ShopState.sozlamalar.set()
    




