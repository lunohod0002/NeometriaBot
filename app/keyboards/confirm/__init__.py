from telebot.types import InlineKeyboardMarkup

from app.keyboards.confirm.button import *

confirm_keyboard = InlineKeyboardMarkup()
confirm_keyboard.row(preliminary_calculation_confirm_button)
confirm_keyboard.row(preliminary_calculation_reject_button)



