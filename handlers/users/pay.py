from aiogram import types
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import *
from states.main import ShopState
from geopy.geocoders import Nominatim
from datetime import datetime
from utils.misc.product import Product




@dp.message_handler(text="Buyurtmalarim 📂", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    await ShopState.tolov.set()
    chizziq = "-"
    user_id = message.from_user.id
    zakaz_nomer = 0

    zakazlar = db.cheak_zakaz(user_id=user_id)
    if len(zakazlar) == 0:
        await message.answer("SIZDA HALI BUYURTMALAR MAVJUD EMAS 🙅")
    else:
        for zakaz in zakazlar:
            zakaz_nomer += 1
            msg = ""
            address = (zakaz[5])[2:-21]

            if zakaz[9] == False:
                tolandi = "To'lanmagan❌"
            else:
                tolandi = "To'langan ✅"

        
            msg += f"<b>📨{zakaz_nomer} - Buyurtma </b>📜\n\nBuyurtma qilingan sana : {zakaz[8]} ⏳\n<i>Buyurtmalar ro'yxati</i> : 🔽<code>\n\n{zakaz[7]}</code>\n{chizziq * 15}\n"
            msg += f"Manzil: {address} 🏙\n{chizziq * 17}\nTelefon raqam : {zakaz[6]} ☎️\nUMUMIY HISOB - {zakaz[2]} 💸\n\n Holati : {tolandi}"
            
            await message.answer(msg)
            await ShopState.category.set()

    