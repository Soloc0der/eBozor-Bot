from aiogram import types
from states.main import *
from loader import dp, db

from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import main_menu, cats_markup, back_btn, cart_btn
from keyboards.default.admin import *

@dp.message_handler(text="ORQAGA 📵", state=ShopState.product)
async def go_cats_menu(message: types.Message):
    cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cats_markup.add(back_btn, cart_btn)
    cats = db.select_all_cats()
    for cat in cats:
        cats_markup.insert(KeyboardButton(text=cat[1]))

    await message.answer("TELEFON TURINI TANLANG !!! 😄", reply_markup=cats_markup)
    await ShopState.category.set()


@dp.message_handler(text="ORQAGA 📵", state=ShopState.admin_panel)
async def go_to_main_menu(message: types.Message):
    await message.answer("ADMIN : 🤖 \n Bo'limlardan birini tanlang :😁", reply_markup=admin)

@dp.message_handler(text="Asosiy menu 🏘",state=ShopState.admin_panel)
async def get_all_users(message: types.Message):
    await ShopState.category.set()
    await message.answer("ADMIN : 🤖 - paneli dan:\nAsosiy bo'limga o'tdingiz 😊", reply_markup=main_menu)



@dp.message_handler(text="ORQAGA 📵", state=ShopState.category)
async def go_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer("BOLIM TANLANG 😊", reply_markup=main_menu)
    await state.finish()

@dp.message_handler(text="ORQAGA 📵", state=ShopState.product)
async def go_cats_menu(message: types.Message):
       #------ cats -----
    all_cats = db.select_all_cats()
    cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cats_markup.row(back_btn, cart_btn)
    for cat in all_cats:
        cats_markup.insert(KeyboardButton(text=cat[1]))
    
    #--------- cats -----


    await message.answer("TELEFON TURINI TANLANG !!! 😄", reply_markup=cats_markup)
    await ShopState.category.set()


@dp.message_handler(text="ORQAGA 📵", state=ShopState.amount)
async def go_to_products_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat_id = data.get("cat_id")

    products = db.select_all_products(cat_id=cat_id)  
    markup_pro = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in products:
        markup_pro.insert(KeyboardButton(text=product[1]))
    markup_pro.row(back_btn, cart_btn)

    await message.answer("Telefon madelini tanlang... 📱", reply_markup=markup_pro)
    await ShopState.product.set()

@dp.message_handler(text="ORQAGA 📵", state=ShopState.cart)
async def go_to_cats_menu(message: types.Message, state: FSMContext):
    await message.answer("Asosiy sahifa 📱", reply_markup=main_menu)
    await state.finish()



dp.message_handler(text="🟥 BEKOR QILISH 🟥", state="*")
async def cancrel_order(message: types.Message, state: FSMContext):
    await message.answer("BUYURTMA BEKOR QILONDI 😥", reply_markup=main_menu)
    await state.finish()

    
dp.message_handler(text="‼️BEKOR QILISH‼️", state=Admin.reklama)
async def cancrel_order(message: types.Message, state: FSMContext):
    await message.answer("reklama BEKOR QILONDI 😥", reply_markup=admin)
    await ShopState.admin_panel.set()

