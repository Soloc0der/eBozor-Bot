from aiogram import types
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import *
from states.main import ShopState
from geopy.geocoders import Nominatim
from datetime import datetime


@dp.message_handler(text="Karzinka 🛒", state="*")
async def get_cart_items(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    items = db.get_all_items(cart_id=cart_id)
    if items:
        msg = "«❌ DEL » - tanlagan telefoni karzinkadan o'chirish\n«🗑 Bo'shatish » - karzinkani bo'shatadi\n\nAyni paytda karzinkada :\n\n"
        total_price = 0
        for item in items:
            data = db.get_product_data(id=item[0])
            price = data[-3] * item[1]
            msg += f"<b>{data[1]} - </b> 📱 \n   {data[-3]} x {item[1]} = {price} so'm ✅\n\n"
            total_price += price
        msg += f"Lar bor 😇\n\nUmumiy hisob: {total_price} so'm"  
        await message.answer(msg, reply_markup=cart_products_murkub(items))
        await ShopState.cart.set()
    else:
        await message.answer("Sizni <b>KARZINKA</b>ngiz hali bo'sh ☹️\nKeling, endi uni qaytadan To'ldiramiz... 🙃", reply_markup=main_menu)
        await state.finish()



@dp.message_handler(text="Tozalash 🗑", state=ShopState.cart)
async def  karzinkani_tozalash(message: types.Message, state : FSMContext):

    # cart id ni topish
    #      VVVV

    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    db.delete_all_product_from_cart(cart_id=cart_id)
    await message.reply("<b>Siz karzinkani tozalab tashladingiz </b>😌\nKeling, endi uni qaytadan To'ldiramiz... 🙃", reply_markup=main_menu)
    await state.finish()





@dp.message_handler(text="Buyurtma berish 📦", state=ShopState.cart)
async def  buyurtma_berish(message: types.Message, state : FSMContext):
    murkub = types.ReplyKeyboardMarkup(resize_keyboard=True)
    murkub.add(phone)
    murkub.add(cancel)
    await message.answer("Buyurtma berish  uchun TELEFON raqamingizni yuboring 🤨\n", reply_markup=murkub)
    
@dp.message_handler(content_types=["contact"], state=ShopState.cart)
async def get_phone_number(message: types.Message, state : FSMContext):
    await state.update_data({
        "phone" : message.contact.phone_number
    })
    murkub = types.ReplyKeyboardMarkup(resize_keyboard=True)
    murkub.add(location)
    murkub.add(cancel)
    await message.answer("TELEFON raqamingiz saqlandi, Endi Joylashuvingizni yuboring 🫡\n", reply_markup=murkub)





@dp.message_handler(content_types=["location"], state=ShopState.cart)
async def get_phone_location(message: types.Message, state: FSMContext):
    full_name = message.from_user.full_name
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data({"lat" : lat,"lon" : lon})
    data = await state.get_data()
    phone = data.get("phone")
    murkub = types.ReplyKeyboardMarkup(resize_keyboard=True)
    adres_topish = Nominatim(user_agent="GetLoc")
    adres = adres_topish.reverse(f"{lat}, {lon}")
    murkub.add(types.KeyboardButton(text="🟢Tastiqlash 🟢"), cancel)
    await message.answer(f"BUYURURTMA BERISH \n\nBuyurtma beruvchi : {full_name}\n\ntelefon raqam : {phone}\n\n YETKAZIB BERISH\n   manzil : <b>{adres}</b>",reply_markup=murkub)


    





@dp.message_handler(text="🟢Tastiqlash 🟢", state=ShopState.cart)
async def tasdiqlash(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lat = data.get("lat")
    lon = data.get("lon")
    phone = data.get("phone")

    adres_topish = Nominatim(user_agent="GetLoc")
    adres = str(adres_topish.reverse(f"{lat}, {lon}"))
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    items = db.get_all_items(cart_id=cart_id)

    total_price = 0

    totol_product = ""
    msg = "📲 HISOB 💳\n"

    for item in items:
        data = db.get_product_data(id=item[0])
        price = data[-3] * item[1]  
        total_price += price
        totol_product += f"{data[1]} : {data[-3]} x {item[1]} = {price} so'm\n"
        msg += f"<code>{data[1]} :   {data[-3]} x {item[1]} = {price} so'm</code>\n\n"
    now = datetime.now()
    ordertime = str(datetime.time(now))
    orderdate = str(datetime.date(now))
    date = f"{orderdate} | {ordertime[:8]}" 
    db.add_order(user_id=user_id, total_price=total_price,lat=lat,lon=lon,adres=adres,phone=phone, totol_product=totol_product, date=date, tolandi=False)
    db.delete_all_product_from_cart(cart_id=cart_id)
    msg += f"umumiy hisob : {total_price}\n\nBUYURTMAGIZ SAQLANDI,\n To'lovni «Buyurtmalarim 📂» bo'limidan qilishingiz mumkin  😸"


    await message.answer(msg, reply_markup=main_menu)
    await state.finish()




@dp.message_handler(state=ShopState.cart)
async def telefonlarni_karzinkadan_ochirish(message: types.Message, state: FSMContext):


    if message.text == "🟥 BEKOR QILISH 🟥":
        await message.answer("BUYURTMA BEKOR QILONDI 😥", reply_markup=main_menu)
        await ShopState.category.set()
    else:
        try:
            katrzinka_tel_list = message.text.split()
            telefon_list = katrzinka_tel_list[1:-1]
            telefon_for = ""
            for i in telefon_list:
                telefon_for += i + " "
                print(telefon_for, type(telefon_for))
            telefon = telefon_for[:-1]
            
            product_id = db.get_product_data(name=telefon)[0]

            user_id = message.from_user.id
            cart_id = db.select_cart(user_id=user_id)[0]

            how_many_in_cart = (db.cheak_cart_product(product_id=int(product_id), cart_id=cart_id))[-2]
            how_many = db.get_product_data(name=telefon)[-2]
            db.delete_product_from_cart(product_id=product_id, cart_id=cart_id)
            db.update_how_many_in_product(how_many=how_many+how_many_in_cart, id=product_id)


            items = db.get_all_items(cart_id=cart_id)
            if items:
                msg = "<b>Ayni paytda karzinkada :</b>\n\n"
                total_price = 0
                for item in items:
                    data = db.get_product_data(id=item[0])
                    price = data[4] * item[1]
                    msg += f"<b>{data[1]} - </b> 📱 \n   {data[4]} x {item[1]} = {price} so'm ✅\n\n"
                    total_price += price
                msg += f"Lar bor 😇\n\nUmumiy hisob: {total_price} so'm" 
                await message.answer(msg, reply_markup=cart_products_murkub(items))
                await ShopState.cart.set()    
            else:
                await message.answer("Sizni <b>KARZINKA</b>ngizni bo'shatdingiz ☹️\n\nKeling endi uni qaytadan To'ldiramiz... 🙃", reply_markup=main_menu)
                await state.finish()
        except:
            await message.answer("Savatcha Da bunday mahsulot mavjud emas...")


