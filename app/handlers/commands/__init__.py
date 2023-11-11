from telebot import TeleBot
import telebot
from app import bot
from app.config import admin_id
from app.keyboards.start import customer_start_keyboard,admin_start_keyboard
from app.services import incurance_property_storage,incurance_live_storage,incurance_live_and_property_storage
@bot.message_handler(content_types=['text'],commands=['start'])
def start(message: telebot.types.Message):
    (message.text)
    if isinstance(message,telebot.types.CallbackQuery):
        incurance_live_and_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
        incurance_live_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
        incurance_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)

    if str(message.text)=="/start":
        if str(message.chat.id)==str(admin_id) :
            bot.send_message(chat_id=message.chat.id,
                         text='Главное меню',
                         reply_markup=admin_start_keyboard)
            incurance_live_and_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
            incurance_live_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
            incurance_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
            incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                          state="incurance_live_and_property")
            incurance_live_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                          state="incurance_live_and_property")
            incurance_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id, state="incurance_live_and_property")


        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Главное меню',
                             reply_markup=customer_start_keyboard)
            incurance_live_and_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
            incurance_live_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
            incurance_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
            incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                          state="incurance_live_and_property")
            incurance_live_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                          state="incurance_live_and_property")
            incurance_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id, state="incurance_live_and_property")
            (incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id))

