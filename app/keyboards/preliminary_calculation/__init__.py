from telebot.types import InlineKeyboardMarkup

from app.keyboards.preliminary_calculation.button import *

preliminary_calculation_keyboard=InlineKeyboardMarkup()
preliminary_calculation_keyboard.row(preliminary_calculation_text_button)
preliminary_calculation_keyboard.row(preliminary_calculation_pdf_button)
