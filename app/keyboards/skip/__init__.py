from telebot.types import InlineKeyboardMarkup

from app.keyboards.skip.button import *
skip_keyboard = InlineKeyboardMarkup()
skip_keyboard.row(skip_button)