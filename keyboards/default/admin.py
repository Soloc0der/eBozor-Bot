from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

admin = ReplyKeyboardMarkup(resize_keyboard=True)
back_btn = KeyboardButton(text="ORQAGA ๐ต")
back_btn = KeyboardButton(text="ORQAGA ๐ต")


bkr_btn = KeyboardButton(text="Bekor qilish ๐")




# reklama

reklama = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
reklama.row("Text ๐ฃ","Photo ๐ผ")
reklama.row(back_btn)




admin.row("Reklama ๐ฃ", "users ๐ฅ")
admin.row("update ๐",  "Tozalash ๐")
admin.row("๐ฉTelefon qo'shish ๐ฉ")
admin.row("Asosiy menu ๐")





admin_del = ReplyKeyboardMarkup(resize_keyboard=True)
admin_del.row("Foydalanuvchilar โ")
admin_del.row("Mahsulotlar ๐ญ")
admin_del.row("Modellar ๐ธ")
admin_del.row("Hammasi โ ๏ธ")
admin_del.row(back_btn)




admin_del_tasdiq = ReplyKeyboardMarkup(resize_keyboard=True)
admin_del_tasdiq.row("Tasdiqlash ๐ข", "Bekor qilish ๐ด")




admin_add_item = ReplyKeyboardMarkup(resize_keyboard=True)
admin_add_item.row("Telefon model ๐")
admin_add_item.row("Telefon ๐ฒ")
admin_add_item.row(back_btn)





add_modell = ReplyKeyboardMarkup(resize_keyboard=True)
add_modell.row("โผ๏ธBEKOR QILISHโผ๏ธ")




# mahsulot qoshish da telefon madellarini korsarish uchun knopka yasash

cats = db.select_all_cats()

cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

for cat in cats:
    cats_markup.insert(KeyboardButton(text=cat[1]))

