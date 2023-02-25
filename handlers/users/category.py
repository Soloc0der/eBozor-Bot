from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.menu import *



@dp.message_handler(state=ShopState.category)
async def get_products_by_category(message: types.Message, state: FSMContext):
    category_name = message.text
    cat_id = db.get_category(name=category_name)[0]



    products = db.select_all_products(cat_id=cat_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in products:
        markup.insert(KeyboardButton(text=product[1]))
    markup.row(back_btn, cart_btn)



    await state.update_data({
        "cat_id": cat_id
    })
    await message.answer(f"{category_name} - Kategoriyasidagi Telefonlar 🫡", reply_markup=markup)
    await ShopState.product.set()
    




