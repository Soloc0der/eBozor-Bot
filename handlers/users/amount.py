from aiogram import types
from states.main import ShopState
from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import numbers
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.menu import back_btn, cart_btn



@dp.message_handler(state=ShopState.amount)
async def get_amount(message: types.Message, state: FSMContext):
    cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cats_markup.add(back_btn, cart_btn)
    cats = db.select_all_cats()
    for cat in cats:
        cats_markup.insert(KeyboardButton(text=cat[1]))

    if message.text.isdigit():
        full_name = message.from_user.full_name
        data = await state.get_data()
        product_id = data.get("product_id")
        product_name = data.get("product_name")
        product_price = data.get("product_price")
        cart_id = data.get("cart_id")
        amount = message.text
        amount = int(amount)
        how_many = db.get_product_data(name=product_name)[-2]


        if how_many == 0:
            await message.answer("Kechirasiz bizda bu mahsulot tugadi 😢", reply_markup=cats_markup)
            await ShopState.category.set()
        else:
            if amount > 0:
                if amount <= how_many:
                    updated_how_many = how_many - amount
                    db.update_how_many_in_product(how_many=updated_how_many, id=product_id)
                    user_cart_products = db.cheak_cart_product(product_id=int(product_id), cart_id=cart_id)
                    print(user_cart_products)
                    if user_cart_products:
                        songi_mahsulot = user_cart_products[2]
                        db.cheaked_card_update(product_id=product_id, quantity = amount + songi_mahsulot, cart_id=cart_id)
                    else:
                        db.add_cart_item(product_id=product_id, quantity=amount, cart_id=cart_id)
                    await message.answer(f"<strong>{amount}ta - {product_name}</strong>\n\n<b>{product_name} x {amount} = {product_price * amount} so'm</b>\n\n<i>Telefon tanlashda davom etamizmi? 😎</i>", parse_mode="html", reply_markup=cats_markup)
                    await bot.send_message(chat_id=ADMINS[0], text=f"{full_name}  # tomonidan\n\n <strong>{amount}  ta  {product_name} </strong> \n\n Karzinkaga qo'shdi ... \nBizda {how_many-amount} ta {product_name} qoldi 😎")
                    await ShopState.category.set()

                else:
                    await message.answer(f"Bizda {amount} - ta {product_name} yo'q \niltimos sal kamroq miqtorni tanlang !!!")
            else:
                await message.answer("Miqdorni to'g'ri raqamlar bilan kiriting ☺️", reply_markup=numbers)
    else:
        await message.answer("iltimos son kiriting !!!")

