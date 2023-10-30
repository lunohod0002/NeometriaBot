from telebot.types import InlineKeyboardMarkup

from app.keyboards.sex.button import *

choose_sex_keyboard=InlineKeyboardMarkup(row_width=2)
choose_sex_keyboard.row(male_button,female_button)
