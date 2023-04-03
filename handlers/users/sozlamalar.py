from aiogram import types, asyncio
from states.main import ShopState
from loader import dp, db, bot
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from geopy import Nominatim



@dp.message_handler(text="Rasm 📸", state=ShopState.sozlamalar)
async def rasmni_sozlash(message: types.Message):
    await message.answer ("Profil uchun O'rnatmoqchi bo'lgan Rasmingizni yuboring :) ", reply_markup=ReplyKeyboardRemove())
    await ShopState.soz_photo.set()

@dp.message_handler(content_types=["photo"], state=ShopState.soz_photo)
async def get_photo(message: types.Message, state: FSMContext):
    print(message)
    soz_photo = message.photo[-1].file_id
    print(soz_photo)
    db.sozlamalar_photo(photo=soz_photo, id=message.from_user.id)
    await message.answer("Yaxshi 😊\nProfil rasmingiz o'zgartirildi...", reply_markup=sozlamalar)
    await ShopState.sozlamalar.set()
    await asyncio.sleep(1)

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

    msg = f"Sizning <b>Profil</b>ingiz ! \n\nIsm: {name} 👤\nUsername: @{username} 📨\n\nTelefon Raqam: {phone} ☎️\n\nJoylashuv: {loc} 🏙"
    await message.answer_photo(photo=photo, caption=msg)




@dp.message_handler(text="Ism 👤", state=ShopState.sozlamalar)
async def rasmni_sozlash(message: types.Message):
    await message.answer ("Profil uchun O'rnatmoqchi bo'lgan <b>ISM</b> ingizni yuboring :) ", reply_markup=ReplyKeyboardRemove())
    await ShopState.soz_name.set()



@dp.message_handler(state=ShopState.soz_name)
async def get_photo(message: types.Message):
    db.sozlamalar_name(name=message.text, id=message.from_user.id)
    await message.answer("Yaxshi 😊\nProfil ISMingiz o'zgartirildi...", reply_markup=sozlamalar)
    await ShopState.sozlamalar.set()
    await asyncio.sleep(1)

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

    msg = f"Sizning <b>Profil</b>ingiz ! \n\nIsm: {name} 👤\nUsername: @{username} 📨\n\nTelefon Raqam: {phone} ☎️\n\nJoylashuv: {loc} 🏙"
    await message.answer_photo(photo=photo, caption=msg)



@dp.message_handler(text="Telefon ☎️", state=ShopState.sozlamalar)
async def  buyurtma_berish(message: types.Message):
    await message.answer("Profil uchun O'rnatmoqchi bo'lgan <b>Telefon Raqamingiz </b> ni yuboring :) 🤨\n", reply_markup=Telefon_btn)
    await ShopState.soz_phone.set()

@dp.message_handler(content_types=["contact"], state=ShopState.soz_phone)
async def get_phone_number(message: types.Message, state : FSMContext):
    phone =  message.contact.phone_number
    db.sozlamalar_phone(phone=phone, id=message.from_user.id)
    await ShopState.sozlamalar.set()
    await asyncio.sleep(1)

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

    msg = f"Sizning <b>Profil</b>ingiz ! \n\nIsm: {name} 👤\nUsername: @{username} 📨\n\nTelefon Raqam: +{phone} ☎️\n\nJoylashuv: {loc} 🏙"
    await message.answer_photo(photo=photo, caption=msg, reply_markup=sozlamalar)



# -------------------------------- Joylashuvni aniqlash ------------------



@dp.message_handler(text="Joylashuv 🏙", state=ShopState.sozlamalar)
async def  buyurtma_berish(message: types.Message):
    await message.answer("<b>Bo'lim lardan</b> birini Tanlang  😌\n", reply_markup=Location_Tanlash)
    await ShopState.soz_loc.set()



@dp.message_handler(text="Avto Aniqlash 📍", state=ShopState.soz_loc)
async def  buyurtma_berish(message: types.Message):
    await message.answer("<b>Avto Aniqlash 📍 </b> Bo'limi tanlandi ✅\n\nBizga o'zingiz turgan joydan Joylashuv yuboring, biz sizni qayerdaligingizni o'zimiz aniqlab olamiz 😼\n\n<b>Jo'naitish 👇</b> tugmasini bosing!", reply_markup=Location_btn)
    await ShopState.soz_loc_auto.set()





@dp.message_handler(content_types=["location"], state=ShopState.soz_loc_auto)
async def get_phone_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    adres_topish = Nominatim(user_agent="GetLoc")
    location = str(adres_topish.reverse(f"{lat}, {lon}"))
    db.sozlamalar_location(loc=location, id=message.from_user.id)
    await ShopState.sozlamalar.set()
    await asyncio.sleep(1)

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


    loc_aniqla = "Nurli yol ko'shesi, Buston MPJ, Qızılyulduz, Mańǵıt, Ámiwdárya rayonı, Qaraqalpaqstan Respublikası, 230700, Oʻzbekiston"
    loc = loc_aniqla.split(sep=", ")
    kocha = loc[0]
    shahar = loc[3]
    tuman = loc[4]
    viloyat = loc[5]
    respublika = loc[7]
    location = f"{respublika} Respublikasi, {viloyat}, {tuman}, {shahar}, {kocha}, ➰"


    if loc == None:
        loc = "Kiritilmagan!"

    msg = f"Sizning <b>Profil</b>ingiz ! \n\nIsm: {name} 👤\nUsername: @{username} 📨\n\nTelefon Raqam: +{phone} ☎️\n\nJoylashuv: {location} 🏙"
    await message.answer_photo(photo=photo, caption=msg, reply_markup=sozlamalar)






@dp.message_handler(text="Yozish ✍️", state=ShopState.soz_loc)
async def  buyurtma_berish(message: types.Message):
    await message.answer("<b>Yozish ✍️ </b> Bo'lim tanlandi ✅ \n\nBizga Ozingiz qayerda ekanligingizni Aniq qilib yozishingiz kerak❗️❕\n<code>Masalan: O''zbekiston RES, *** tuman, *** shahar, ** ko'cha, ??-uy</code>\n\n⚠️ Ogohlantirish Manzilni Xato kiritish jiddiy Muammmolarga sabab bo'lishi mumkin ⚠️", reply_markup=ReplyKeyboardRemove())
    await ShopState.soz_loc_write.set()


@dp.message_handler(state=ShopState.soz_loc_write)
async def get_photo(message: types.Message):
    db.sozlamalar_location(loc=message.text, id=message.from_user.id)
    await message.answer("Yaxshi 😊\nProfil Manzilingiz o'zgartirildi...", reply_markup=sozlamalar)
    await ShopState.sozlamalar.set()
    await asyncio.sleep(1)
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

    msg = f"Sizning <b>Profil</b>ingiz ! \n\nIsm: {name} 👤\nUsername: @{username} 📨\n\nTelefon Raqam: {phone} ☎️\n\nJoylashuv: {loc} 🏙"
    await message.answer_photo(photo=photo, caption=msg)
    

