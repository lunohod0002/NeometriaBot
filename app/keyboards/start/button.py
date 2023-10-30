from telebot.types import InlineKeyboardButton

from app.keyboards.start.text import *

insurance_live_button = InlineKeyboardButton(text=insurance_live_button_info.text,
                                         callback_data=insurance_live_button_info.callback_data)

insurance_live_and_property_button = InlineKeyboardButton(text=insurance_live_and_property_button_info.text,
                                         callback_data=insurance_live_and_property_button_info.callback_data)
insurance_property_button = InlineKeyboardButton(text=insurance_property_button_info.text,
                                         callback_data=insurance_property_button_info.callback_data)

executed_documents_button = InlineKeyboardButton(text=executed_documents_button_info.text,
                                         callback_data=executed_documents_button_info.callback_data)
downlad_documents_button=InlineKeyboardButton(text=download_dicuments_button_info.text,
                                         callback_data=download_dicuments_button_info.callback_data)