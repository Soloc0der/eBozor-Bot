from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

main_menu.row("PHONE 📱")
main_menu.row("Karzinka 🛒", "Buyurtmalarim 📂")
main_menu.row("Sozlamalar ⚙️", "Hamyonim 💰")

back_btn = KeyboardButton(text="ORQAGA 📵")
cart_btn = KeyboardButton(text="Karzinka 🛒")   


cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
cats = db.select_all_cats()



for cat in cats:
    cats_markup.insert(KeyboardButton(text=cat[1]))
cats_markup.add(back_btn, cart_btn)




# def make_products_markup(cat_id):
#     products = db.select_all_products(cat_id=cat_id)  
#     markup.add(back_btn, cart_btn)
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     for product in products:
#         markup.insert(KeyboardButton(text=product[1]))
#     return markup


numbers = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)    

for num in range(1, 10):
    numbers.insert(KeyboardButton(text=str(num)))
numbers.add(back_btn)




phone = KeyboardButton(text="TELEFON RAQAMNI ☎️", request_contact=True)
location = KeyboardButton(text="JOYLASHUV 📍", request_location=True)
cancel = KeyboardButton(text="🟥 BEKOR QILISH 🟥")  



def cart_products_murkub(items):
    murkub = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in items:
        data = db.get_product_data(id=item[0])
        murkub.insert(KeyboardButton(f"❌ {data[1]} x{item[1]}"))
    murkub.add("Tozalash 🗑", back_btn)
    murkub.add(KeyboardButton(text="Buyurtma berish 📦"))
    return murkub


