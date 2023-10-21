from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


kb = [
    [KeyboardButton(text="/help")],
    [KeyboardButton(text="/familia")],
    [KeyboardButton(text="/fio")],
    [KeyboardButton(text="/kab")],
    [KeyboardButton(text="/email")],
    [KeyboardButton(text="/tel")]
]

menuKeyboard = ReplyKeyboardMarkup(keyboard=kb)