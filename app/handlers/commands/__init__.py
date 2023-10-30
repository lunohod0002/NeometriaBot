from telebot import TeleBot
import telebot
from app import bot
from app.config import admin_id
from app.keyboards.start import customer_start_keyboard,admin_start_keyboard
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    if str(message.chat.id)==str(admin_id):
        bot.send_message(chat_id=message.chat.id,
                     text='Главное меню',
                     reply_markup=customer_start_keyboard)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Главное меню',
                         reply_markup=customer_start_keyboard)

