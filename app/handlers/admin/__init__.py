import telebot.types
from app.config import admin_id
from app import bot
from telebot.types import CallbackQuery, Message
from app.services import incurance_live_storage
from app.keyboards.start.text import insurance_live_button_info,download_dicuments_button_info
from app.API.PDF import PDF
import os
@bot.callback_query_handler(func=lambda call: download_dicuments_button_info.filter(call.data))
def send_tg_id(call: CallbackQuery):
    bot.send_message(chat_id=admin_id,
                          text='Напишите id/ник/номер телефона пользователя телеграмм')

    def download_document(message: Message):

        tg_id = 0

        with open('users.txt','r') as f:
            for line in f:
                s=line.rstrip()
                s=s.split("[]")
                for sym in s:
                    if message.text in sym:
                        tg_id=s[0]
                        break
        if tg_id==0:
            bot.send_message(chat_id=admin_id,
                             text='Пользователь не найден')
        else:
            bot.send_message(chat_id=admin_id,
                             text='Загрузите оформленный документ pdf')
            def send_offer_document(message:Message):
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(message.document.file_name, 'wb') as f:
                    f.write(downloaded_file)

                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                    key=message.document.file_name,
                                    catalog="issued_documents")
                mas = pdf.download_document(message.chat.id, "issued_documents")
                bot.send_document(tg_id,open(mas[0],"rb"))
                bot.send_message(chat_id=admin_id,
                                 text='Документ отправлен')




            bot.register_next_step_handler(message, send_offer_document)

    bot.register_next_step_handler(call.message, download_document)

