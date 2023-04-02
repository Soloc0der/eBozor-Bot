import logging
from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data.config import ADMINS







@dp.message_handler(text="Bot Haqida 📴", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    await state.finish()
    about_message = f"Assalomu aleykum  😊\n\nBu Bo't *** - Do'konining rasmiy bo'ti ✅\nBo't orqali Tez va Qulay tarizda ~Telefon~ sotib olishingiz mumkin🤩📲\n\nIltimos Bo'limlardan birini tanlang..."
    await message.answer(about_message, reply_markup=about)
    await ShopState.about.set()




@dp.message_handler(text="Statistika 📊", state=ShopState.about)
async def  Statistic(message: types.Message):
    users_count = db.count_users()[0]
    cats_count = db.count_cats()[0]
    product_count = db.count_products()[0]

    msg = f"Assalomu aleykum  🐵\n\nBot Statistikasi 📊\n\nFoydalanuvchilar: {users_count} 🙍🏻\nModellar: {cats_count} 🍏\nMahsulotlar: {product_count} 📱\n\n  Qo'shimcha Ma'lumotlar uchun admin ga Murojat qiling ✅"
    await message.answer(msg)


@dp.message_handler(text="Admin 👮", state=ShopState.about)
async def admin(message: types.Message):
    msg = f"Bo't Haqida Qandaydur Muammo bo'layotgan bo'lsa tezda Admin 👮 bilan bo'g'lanishingizni so'raymiz ❕\n\nUlar sizga  8 soat ⏰  ichida javob beradi ✅\n\nAdminlar: \n   @solo_Junior 🔰\n   @solo_coder 🔰\n   @Khurshid_off 🔰"
    await message.answer(msg)



@dp.message_handler(text="Fikr qoldirish 〽️", state=ShopState.about)
async def admin(message: types.Message):
    msg = f"Bot AdminlariGa Muammo yoki Takliflar uchun fikir qoldirishingiz mumkin ❇️\n\nYubormoqchi bo'lgan fikringiz [1000] ta Harfdan Ko'p Bo'lmasligi kerak ⁉️\n\nfikringiz Adminlarga yuboriladi va Juda tez fursatda ko'rib chiqiladi ✔️\n\nfikr uchun oldindan Raxmat 🤝"
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())
    await ShopState.about_faq.set()

@dp.message_handler(state=ShopState.about_faq)
async def FAQ(message: types.Message):
    user = message.from_user.full_name
    id = message.from_user.id
    text = message.text
    print(len(text))
    if len(text) <= 1000:
        msg = f"{id}\nfoydalanuvchi: -- {user} -- fikr qoldirdi 🤝\n\n{text}"
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, msg)

            except Exception as err:
                logging.exception(err)

        await message.answer("fikringiz Adminlarga yetkazildi 🥳\n\nfikr uchun raxmat 🤝", reply_markup=about)
        await ShopState.about.set()
    else:
        await message.answer("iltimos Fikringizni Sal qisqaroq qiling\n\n: 1000 Harf dan kop yozmang ❕")
