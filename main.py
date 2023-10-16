import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from parsing import searcWorker


TOKEN = '6392740543:AAEAznA8-Zjh5c1XcFJeZOScRLDXgbJFe5Y'

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


# @dp.message(Command("fio"))
# async def command_fio_handler(message: types.Message):


@dp.message()
async def command_fio_handler(message: types.Message):
    inputUser = message.text
    answer = searcWorker(inputUser)
    for a in answer:
        await message.answer(a, parse_mode="html")
    await message.answer("Вводи следующие ФИО")




async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())