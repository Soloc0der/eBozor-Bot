from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

admin = ReplyKeyboardMarkup(resize_keyboard=True)
back_btn = KeyboardButton(text="ORQAGA 📵")
photo_back = KeyboardButton(text="ORQAGA 📵")

bkr_btn = KeyboardButton(text="Bekor qilish 📄")




# reklama

reklama = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
reklama.row("Text 📣","Photo 🖼")
reklama.row(back_btn)




admin.row("Reklama 📣", "users 👥")
admin.row("update 🆙",  "Tozalash 🗑")
admin.row("🟩Telefon qo'shish 🟩")
admin.row("Asosiy menu 🏘")





admin_del = ReplyKeyboardMarkup(resize_keyboard=True)
admin_del.row("Foydalanuvchilar ❌")
admin_del.row("Mahsulotlar 💭")
admin_del.row("Modellar 🔸")
admin_del.row("Hammasi ⚠️")
admin_del.row(back_btn)




admin_del_tasdiq = ReplyKeyboardMarkup(resize_keyboard=True)
admin_del_tasdiq.row("Tasdiqlash 🟢", "Bekor qilish 🔴")




admin_add_item = ReplyKeyboardMarkup(resize_keyboard=True)
admin_add_item.row("Telefon model 🆒")
admin_add_item.row("Telefon 📲")
admin_add_item.row(back_btn)





add_modell = ReplyKeyboardMarkup(resize_keyboard=True)
add_modell.row("‼️BEKOR QILISH‼️")




# mahsulot qoshish da telefon madellarini korsarish uchun knopka yasash

cats = db.select_all_cats()

cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

for cat in cats:
    cats_markup.insert(KeyboardButton(text=cat[1]))

