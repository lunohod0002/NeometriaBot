from telebot.types import InlineKeyboardButton

from app.keyboards.skip.text import *

skip_button = InlineKeyboardButton(text=skip_button_info.text,
                                         callback_data=skip_button_info.callback_data)
