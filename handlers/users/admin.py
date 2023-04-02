import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from states.main import *
from keyboards.default.admin import *
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import main_menu
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text


cnt = 4
foydalanuvchilar = db.count_users()[0]



@dp.message_handler(text="/admin", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await ShopState.admin_panel.set()
    await message.answer("ADMIN : 🤖 - paneliga xush kelibsiz 😇\n\nBo'limni tanlang :", reply_markup=admin)



@dp.message_handler(text="users 👥", user_id=ADMINS, state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       


@dp.message_handler(text="update 🆙", user_id=ADMINS, state=ShopState.admin_panel)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="Bot yangilandi😍\n\nbotdan foydalanish uchun qaytadan /start buyrug'ini bering...")
        await asyncio.sleep(0.05)



@dp.message_handler(Text(startswith="/update"), user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    vertion = message.text[7:]
    msg = f"Bot Yangilandi🎉\n\nVertion: {vertion} ✅\n\nYangilanishdan Keyin bot yanada yaxshiroq ishlaydi 😎"
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text=msg)
        await asyncio.sleep(0.05)



#      admin panelida tozalash !!!



@dp.message_handler(text="Tozalash 🗑", user_id=ADMINS,state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await message.answer("<b>Foydalanuvchilar ❌ </b> - Foydalanuvchilarni tozalash\n<b>Hammasi ⚠️</b> - Bazadan Bot xamma maulumotlarini tozalash \n<code>(Tavsiya etilmaydi ‼️)</code>", reply_markup=admin_del)



# admin paneli dan foydalanuvchilarni o'chirish ---------------------



@dp.message_handler(text="Foydalanuvchilar ❌", user_id=ADMINS, state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await message.answer(f"Haqiqatdan ham botdan foydalanuvchilarni tozalamoqchimisiz???\nBazada {foydalanuvchilar} - ta foydalanuvchi bor", reply_markup=admin_del_tasdiq)
    await Admin.del_users.set()



@dp.message_handler(text="Tasdiqlash 🟢", user_id=ADMINS, state=Admin.del_users)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Bazadan foydalanuvchilar tozalandi ✅", reply_markup=admin)
    await ShopState.admin_panel.set()



@dp.message_handler(text="Bekor qilish 🔴", user_id=ADMINS, state=Admin.del_users)
async def get_all_users(message: types.Message):
    await message.answer("❌ Bazadan foydalanuvchilar tozalash Bekor qilindi 🔴❌", reply_markup=admin)
    await ShopState.admin_panel.set()



###########################################################################



@dp.message_handler(text="Tasdiqlash 🟢", user_id=ADMINS, state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Bazadan foydalanuvchilar tozalandi ✅", reply_markup=admin)



@dp.message_handler(text="Bekor qilish 🔴", user_id=ADMINS, state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await message.answer("❌ Bazadan foydalanuvchilar tozalash Bekor qilindi 🔴❌", reply_markup=admin)



#_______________############################################_______________
#                   admindan product ni ochirish



@dp.message_handler(text="Mahsulotlar 💭", user_id=ADMINS, state=ShopState.admin_panel)
async def open_del_products_from_admin(message: types.Message):
    
    #------ cats -----
    admin_cats = db.select_all_cats()
    admin_cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for cat in admin_cats:
        admin_cats_markup.insert(KeyboardButton(text=cat[1]))
    #--------- cats ----

    await message.answer("Qaysi model turidan o'cjirmoqchisiz?", reply_markup=admin_cats_markup)
    await Admin.del_products_cat.set()



@dp.message_handler(user_id=ADMINS, state=Admin.del_products_cat)
async def del_products_from_admin(message: types.Message):

    category_name = message.text
    cat_id = db.get_category(name=category_name)[0]

    products = db.select_all_products(cat_id=cat_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in products:
        markup.insert(KeyboardButton(text=product[1]))

    await message.answer("O'chirmoqchi bo'lgan mahsulotingizni tanlang ", reply_markup=markup)
    await Admin.del_products_pro.set()



@dp.message_handler(user_id=ADMINS, state=Admin.del_products_pro)
async def get_all_users(message: types.Message):
    name = message.text
    product_id = db.get_product_data(name=name)[0]
    print(type(product_id))
    db.delete_product_from_admin(id=product_id)

    await message.answer("Mahsulot muvifaqiyatli o'chirildi ", reply_markup=admin)
    await ShopState.admin_panel.set()


#_______________############################################_______________
#                   admindan category ni ochirish



@dp.message_handler(text="Modellar 🔸", user_id=ADMINS, state=ShopState.admin_panel)
async def open_del_products_from_admin(message: types.Message):
    


    #------ cats -----
    admin_cats = db.select_all_cats()
    admin_cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for cat in admin_cats:
        admin_cats_markup.insert(KeyboardButton(text=cat[1]))
    #--------- cats ----

    await message.answer("O'chirmoqchi bo'lgan modelin gizni tanlang ", reply_markup=admin_cats_markup)
    await Admin.del_cats.set()



@dp.message_handler(user_id=ADMINS, state=Admin.del_cats)
async def del_products_from_admin(message: types.Message):

    cat_name = message.text
    cat_data = db.get_cat_data(name=cat_name)
    max_cat_id = cat_data[0]

    db.delete_categoryes(id=max_cat_id)
    await message.answer(f"{cat_name} Modeli muvofaqiyatli ✅", reply_markup=admin)
    await ShopState.admin_panel.set()



#----------------------------  hammasini ochirish !!!!!!!!!!!!!!!!!!!!!!!!!!!!



@dp.message_handler(text="Hammasi ⚠️", user_id=ADMINS, state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await message.answer(f"🟥🟥🟥🟥🟥🟥🟥🟥🟥\n❗️❗️❗️❗️❗️❗️❗️❗️❗️\n\nOgoxlantirish bu tasdiqlashni bossangiz Bot bazasi butunlay tozalanadi !!!\nyani foydalanuvchilar toyxati\nmahsulotlar va modellar\n\nQaytaraman <code>(Tavsiya etilmaydi ‼️)</code>\n\n❗️❗️❗️❗️❗️❗️❗️❗️❗️\n🟥🟥🟥🟥🟥🟥🟥🟥🟥", reply_markup=admin_del_tasdiq)
    await Admin.del_all.set()



@dp.message_handler(text="Tasdiqlash 🟢", user_id=ADMINS, state=Admin.del_all)
async def get_all_users(message: types.Message):
    db.delete_users()
    db.delete_cats()
    db.delete_products()
    db.delete_Cart_items()
    db.delete_Carts()
    db.delete_profiles()
    await message.answer("Bazadan Hammasi tozalandi ✅", reply_markup=admin)
    await ShopState.admin_panel.set()

@dp.message_handler(text="Bekor qilish 🔴", user_id=ADMINS, state=Admin.del_all)
async def get_all_users(message: types.Message):
    await message.answer("❌ Bazadan Hammasini tozalash Bekor qilindi 🔴❌", reply_markup=admin)
    await ShopState.admin_panel.set()



#------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



# =============================================          REKLAMA       ===================



@dp.message_handler(text="Reklama 📣", user_id=ADMINS, state=ShopState.admin_panel)
async def reklamasorash(message: types.Message):
    await message.answer("Reklama bo'limiga o'tdingiz 😁\n\nFoydalanuvchilarga tarqatmoqchi bo'lgan REKLAMA ngizni tarqatiladi \n\nQanday reklama tarqatmoqchisiz?\n\nTEXT :?\n\nPHOTO :? 🤝", reply_markup=reklama)
    # await message.reply("test", reply_markup=reklama)
    await Admin.reklama.set()



@dp.message_handler(text="Text 📣", user_id=ADMINS, state=Admin.reklama)
async def reklamatext(message: types.Message):
    await message.answer("Reklama bo'limiga o'tdingiz 😁\n\nFoydalanuvchilarga tarqatmoqchi bo'lgan REKLAMA ngizni Text korinishida menga yuboring 😎", reply_markup=photo_back)
    await Admin.text_rek.set()



@dp.message_handler(user_id=ADMINS, state=Admin.text_rek)
async def reklamatexttarqat(message: types.Message):
    if message.text == "ORQAGA 📵":
        await message.answer("Reklama berish Bekor qilindi!", reply_markup=admin)
        await ShopState.admin_panel.set()
    else:
        msg = message.text
        users = db.select_all_users()
        for user in users:
            user_id = user[0]
            await bot.send_message(chat_id=user_id, text=msg)
            await asyncio.sleep(0.05)
        await bot.send_message(chat_id=ADMINS[0], text="Reklama xammaga tarqatildi 🙋‍♂️", reply_markup=admin)
        await ShopState.admin_panel.set()



@dp.message_handler(text="Photo 🖼", user_id=ADMINS, state=Admin.reklama)
async def reklamaphoto(message: types.Message):
    await message.answer("Reklama bo'limiga o'tdingiz 😁\n\nFoydalanuvchilarga tarqatmoqchi bo'lgan REKLAMA ngizni # Rasm # korinishida menga yuboring 😎\n {text ishlatsa xam bolad }", reply_markup=photo_back)
    await Admin.photo_rek.set()



@dp.message_handler(content_types=["photo"], state=Admin.photo_rek)
async def get_photoreklama(message: types.Message):
    msg = message.caption
    photo = message.photo[-1].file_id
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_photo(chat_id=user_id, photo=photo, caption=msg)
        await asyncio.sleep(0.05)

    await ShopState.admin_panel.set()
    await bot.send_message(chat_id=ADMINS[0], text="Reklama xammaga tarqatildi 🙋‍♂️", reply_markup=admin)



#    Mahsulot qo'shish ~!!!



@dp.message_handler(text="🟩Telefon qo'shish 🟩", user_id=ADMINS,state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await message.answer("<b>Telefon qo'shish bo'limi 😌</b>", reply_markup=admin_add_item)



# admin panelidan model qo'shish  --------------------------------------------------------------------------



@dp.message_handler(text="Telefon model 🆒", user_id=ADMINS,state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await message.answer("<b>Telefon Modelini qo'shish bo'limiga xush kelibsiz 😁</b>\n\nDemak tushuntiraman: \n\n   Siz yangi xozir Telefon modelini kiritishingiz kerak", reply_markup=add_modell)
    await ShopState.insert_category.set()



@dp.message_handler(user_id=ADMINS, state=ShopState.insert_category)
async def get_all_users(message: types.Message, state: FSMContext):

    name = message.text
    cnt_cats = db.select_all_cats()
    if len(cnt_cats) == 0:
        print(cnt_cats)
        cat_id = 1
    else:
        cat_id = (db.select_all_cats()[-1][-1]) + 1
    db.admin_add_cats(name=name, cat_id=cat_id)
    await message.reply(f"{name} - bazaga muvofaqiyatli qo'shildi ✅✅", reply_markup=admin)
    await ShopState.admin_panel.set()
    


#-----------------------------------------------------------------------------------------------------



# admin panelidan maxsulot qo'shish



@dp.message_handler(text="Telefon 📲", user_id=ADMINS, state=ShopState.admin_panel)
async def get_all_users(message: types.Message):

    await message.answer("<b>Telefon Qo'shish bo'limi ... </b>\n\nDemak tushuntiraman: \n\n   Siz yangi telefon qo'shmoqchisiz\n\nbunda sizdan talab qilinad:\nMahsulot Nomi ?\nMahsulot haqida ?\nMahsulot rasmi ?\nMahsulot Bahosi ? \nMahsulotdan nechta mavjud ekanligi ?\nMahsulot qaysi model dan ekanligi ?\n\nXozir Mahsulot - Nomini - kiriting ...", reply_markup=add_modell)
    await Admin.get_name.set()



@dp.message_handler(state=Admin.get_name)
async def product_desc(message: types.Message, state: FSMContext):
    max_name = message.text
    await state.update_data({
        "max_name": max_name
    })
    await message.answer(f"Endi Mahsulot ma'lumotlarini kiriting...")
    await Admin.get_desc.set()



@dp.message_handler(state=Admin.get_desc)
async def product_desc(message: types.Message, state: FSMContext):
    max_desc = message.text
    await state.update_data({
        "max_desc": max_desc
    })
    await message.answer(f"Endi Mahsulot Rasmini Yuboring...!!!")
    await Admin.get_photo.set()



@dp.message_handler(content_types=["photo"], state=Admin.get_photo)
async def get_photo(message: types.Message, state: FSMContext):
    max_photo = message.photo[-1].file_id
    await state.update_data({
        "max_photo": max_photo
    })
    await message.answer("Yaxshi 😊\nMahsulot narxini kiriting...\n\n(faqat son korinishida!!!)")
    await Admin.get_price.set()



@dp.message_handler(state=Admin.get_price)
async def product_desc(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        max_price = message.text
        await state.update_data({
            "max_price": max_price
        })
        await message.answer(f"Endi Mahsulot miqdorini yani qancha ekanligini Yuboring...!!!")
        await Admin.get_hm.set()
    else:
        await message.answer(f"Iltimos Narxni Butun Son ko'rinishida yozing...\n\n (. , - ishlatilmasin)")
    


@dp.message_handler(state=Admin.get_hm)
async def product_desc(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        max_hm = message.text
        await state.update_data({
            "max_hm": max_hm
        })
            #------ cats -----
        admin_cats = db.select_all_cats()
        admin_cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for cat in admin_cats:
            admin_cats_markup.insert(KeyboardButton(text=cat[1]))
        #--------- cats -----



        await message.answer(f"Endi Mahsulot qaysi model dan ekanligi TANLANG...!!!", reply_markup=admin_cats_markup)
        await Admin.get_cat_id.set()

    else:
        await message.answer(f"Iltimos Narxni Butun Son ko'rinishida yozing...\n\n (. , - ishlatilmasin)")


 


@dp.message_handler(state=Admin.get_cat_id)
async def cat(message: types.Message, state: FSMContext):
    cat_name = message.text
    cat_data = db.get_cat_data(name=cat_name)
    max_cat_id = cat_data[0]
    await state.update_data({
        "max_cat_id": max_cat_id
    })



    data = await state.get_data()
    max_name = data["max_name"]
    max_desc = data["max_desc"]
    max_photo = data["max_photo"]
    max_price = data["max_price"]
    max_hm = data["max_hm"]
    max_cat_id = data["max_cat_id"]
    db.add_products(name=max_name, desc=max_desc, image=max_photo, price=max_price,how_many=max_hm, cat_id=max_cat_id)
    msg = (f"Yangi mahsulot: \nMahsulot Nomi {max_name}\nMahsulot haqida: \n{max_desc}\n\nMahsulot Bahosi {max_price} \nMahsulotdan nechta mavjud ekanligi {max_hm}\nMahsulot qaysi model dan ekanligi {cat_name}")
    await message.answer_photo(photo=max_photo, caption=msg, reply_markup=admin)
    await ShopState.admin_panel.set()

