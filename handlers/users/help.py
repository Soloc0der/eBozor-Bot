from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("ASSALOMU ALEYKUM \n BU BOT SIZGA TELEFON SOTIB OLISHDA YORDAM BERADI )")
    await message.answer(text)
