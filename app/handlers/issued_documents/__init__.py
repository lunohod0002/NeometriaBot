import telebot.types
from app.config import admin_id
from app import bot
from telebot.types import CallbackQuery, Message
from app.services import incurance_live_storage
from app.keyboards.start.text import insurance_live_button_info,download_dicuments_button_info,executed_documents_button_info
from app.API.PDF import PDF
import os
@bot.callback_query_handler(func=lambda call: executed_documents_button_info.filter(call.data))
def send_tg_id(call: CallbackQuery):
    pdf=PDF()
    mas = pdf.download_document(call.message.chat.id, "issued_documents")
    if (mas is None and mas==None):
        bot.send_message(chat_id=call.message.chat.id,
                         text='У вас нет оформленных документов')
    else:
        bot.send_message(chat_id=call.message.chat.id,text="Ваши документы")

        for i in mas:
            bot.send_document(call.message.chat.id,open(i,'rb'))


