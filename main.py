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
    updateDB, searchInDB
from stringConversion import conversionFIOToFamilia, conversionFIO, deleteSpace

from message import START_MESSAGE, HELP_MESSAGE
    

PATH_DB = 'data base.db'

TOKEN = '6392740543:AAEAznA8-Zjh5c1XcFJeZOScRLDXgbJFe5Y'

dp = Dispatcher()
connection = createConnection(PATH_DB)

class FindFamilia(StatesGroup):
    find = State()

class FindFIO(StatesGroup):
    find = State()

class FindKab(StatesGroup):
    find = State()

class FindTelefon(StatesGroup):
    find = State()

class FindEmail(StatesGroup):
    find = State()


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(START_MESSAGE)

@dp.message(Command("help"))
async def command_familia(message: types.Message, state: FSMContext):
    await message.answer(HELP_MESSAGE)


@dp.message(Command("familia"))
async def command_familia(message: types.Message, state: FSMContext):
    await state.set_state(FindFamilia.find)
    await message.answer("Введите фамилию:")
    


@dp.message(FindFamilia.find)
async def find_familia(message: types.Message, state: FSMContext):
    inputUser = message.text
    inputUser = conversionFIOToFamilia(inputUser)
    answer = searchInDB(connection, inputUser, "familia")
    if answer == None:
        await message.answer("Ошибка!")
    elif len(answer) == 0:
        await message.answer("Ничего не найдено!")
    else:
        for ans in answer:
            await message.answer(ans[0], parse_mode="html")
    await state.clear()


@dp.message(Command("fio"))
async def command_fio(message: types.Message, state: FSMContext):
    await state.set_state(FindFIO.find)
    await message.answer("Введите ФИО:")

@dp.message(FindFIO.find)
async def find_fio(message: types.Message, state: FSMContext):
    inputUser = message.text
    inputUser = conversionFIO(inputUser)
    answer = searchInDB(connection, inputUser, "fio")
    if answer == None:
        await message.answer("Ошибка!")
    elif len(answer) == 0:
        await message.answer("Ничего не найдено!")
    else:
        for ans in answer:
            await message.answer(ans[0], parse_mode="html")
    await state.clear()


@dp.message(Command("kab"))
async def command_kab(message: types.Message, state: FSMContext):
    await state.set_state(FindKab.find)
    await message.answer("Введите номер кабинета:")

@dp.message(FindKab.find)
async def find_kab(message: types.Message, state: FSMContext):
    inputUser = message.text
    inputUser = deleteSpace(inputUser)
    answer = searchInDB(connection, inputUser, "kab")
    if answer == None:
        await message.answer("Ошибка!")
    elif len(answer) == 0:
        await message.answer("Ничего не найдено!")
    else:
        for ans in answer:
            await message.answer(ans[0], parse_mode="html")
    await state.clear()



@dp.message(Command("email"))
async def command_email(message: types.Message, state: FSMContext):
    await state.set_state(FindEmail.find)
    await message.answer("Введите E-mail:")

@dp.message(FindEmail.find)
async def find_email(message: types.Message, state: FSMContext):
    inputUser = message.text
    inputUser = deleteSpace(inputUser)
    answer = searchInDB(connection, inputUser, "email")
    if answer == None:
        await message.answer("Ошибка!")
    elif len(answer) == 0:
        await message.answer("Ничего не найдено!")
    else:
        for ans in answer:
            await message.answer(ans[0], parse_mode="html")
    await state.clear()


@dp.message(Command("tel"))
async def command_tel(message: types.Message, state: FSMContext):
    await state.set_state(FindTelefon.find)
    await message.answer("Введите номер телефона:")

@dp.message(FindTelefon.find)
async def find_tel(message: types.Message, state: FSMContext):
    inputUser = message.text
    inputUser = deleteSpace(inputUser)
    answer = searchInDB(connection, inputUser, "tel")
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