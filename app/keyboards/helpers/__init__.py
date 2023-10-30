from telebot.types import ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup

from telebot.types import KeyboardButton

share_contact_button = KeyboardButton(text='Поделиться номером телефона', request_contact=True)

share_contact_keyboard = ReplyKeyboardMarkup()

share_contact_keyboard.row(share_contact_button)


share_contact_keyboard.row(share_contact_button)
