from telebot.types import InlineKeyboardButton

from app.keyboards.sex.text import *

male_button = InlineKeyboardButton(text=male_button_info.text,
                                         callback_data=male_button_info.callback_data)

female_button = InlineKeyboardButton(text=female_button_info.text,
                                         callback_data=female_button_info.callback_data)
