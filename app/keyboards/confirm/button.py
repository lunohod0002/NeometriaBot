from telebot.types import InlineKeyboardButton

from app.keyboards.confirm.text import *

preliminary_calculation_confirm_button = InlineKeyboardButton(text=preliminary_calculation_confirm_button_info.text,
                                         callback_data=preliminary_calculation_confirm_button_info.callback_data)

preliminary_calculation_reject_button = InlineKeyboardButton(text=preliminary_calculation_reject_button_info.text,
                                         callback_data=preliminary_calculation_reject_button_info.callback_data)
