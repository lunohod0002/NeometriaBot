from telebot.types import InlineKeyboardButton

from app.keyboards.preliminary_calculation.text import *

preliminary_calculation_pdf_button = InlineKeyboardButton(text=preliminary_calculation_pdf_button_info.text,
                                         callback_data=preliminary_calculation_pdf_button_info.callback_data)

preliminary_calculation_text_button = InlineKeyboardButton(text=preliminary_calculation_text_button_info.text,
                                         callback_data=preliminary_calculation_text_button_info.callback_data)
