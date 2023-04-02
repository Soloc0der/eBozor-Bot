from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

main_menu.row("PHONE 📱")
main_menu.row("Karzinka 🛒", "Buyurtmalarim 📂")
main_menu.row("Sozlamalar ⚙️", "Bot Haqida 📴")

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
    murkub.add("Tozalash 🗑","Buyurtma berish 📦")
    murkub.add(back_btn)
    return murkub





sozlamalar = ReplyKeyboardMarkup(resize_keyboard=True)
sozlamalar.row("Rasm 📸", "Ism 👤")
sozlamalar.row("Telefon ☎️", "Joylashuv 🏙")
sozlamalar.add(back_btn)


soz_phone = KeyboardButton(text="Yuborish ☎️", request_contact=True)
soz_location = KeyboardButton(text="Yuborish 📍", request_location=True)
soz_cancel = KeyboardButton(text="Bekor Qilish🟥")  

Telefon_btn = ReplyKeyboardMarkup(resize_keyboard=True)
Telefon_btn.add(soz_phone)
Telefon_btn.add(soz_cancel)


Location_Tanlash = ReplyKeyboardMarkup(resize_keyboard=True)
Location_Tanlash.row("Avto Aniqlash 📍")
Location_Tanlash.row("Yozish ✍️")
Location_Tanlash.add(soz_cancel)


Location_btn = ReplyKeyboardMarkup(resize_keyboard=True)
Location_btn.add(soz_location)
Location_btn.add(soz_cancel)







about = ReplyKeyboardMarkup(resize_keyboard=True)
about_cancel = KeyboardButton(text="Orqaga 🔙")

about.row("Statistika 📊", "Admin 👮")
about.row("Fikr qoldirish 〽️")
about.row("Biz HaqimiZda ⚜️", about_cancel)


