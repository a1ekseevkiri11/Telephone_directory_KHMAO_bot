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
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db import createConnection, executeQuery, \
    updateDB, searchFIOInDB, searchFamiliaInDB
from stringConversion import conversionFIOToFamilia, conversionFIO
    

PATH_DB = 'data base.db'

TOKEN = '6392740543:AAEAznA8-Zjh5c1XcFJeZOScRLDXgbJFe5Y'

dp = Dispatcher()
connection = createConnection(PATH_DB)

class FindFamilia(StatesGroup):
    find = State()


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command("familia"))
async def command_familia(message: types.Message, state: FSMContext):
    await state.set_state(FindFamilia.find)
    await message.answer("Введите фамилию: ")
    


@dp.message(FindFamilia.find)
async def find_familia(message: types.Message, state: FSMContext):
    inputUser = message.text
    inputUser = conversionFIOToFamilia(inputUser)
    answer = searchFamiliaInDB(connection, inputUser)
    if answer == None:
        await message.answer("Ошибка!")
    elif len(answer) == 0:
        await message.answer("Ничего не найдено!")
    else:
        for ans in answer:
            await message.answer(ans[0], parse_mode="html")
    await state.clear()





async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    updateDB(connection)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())