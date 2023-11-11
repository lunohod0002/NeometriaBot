import telebot.types
from app.keyboards.helpers import share_contact_keyboard
from app import bot
from app.API.PDF import PDF
from telebot.types import CallbackQuery, Message
from app.keyboards.sex import choose_sex_keyboard, female_button_info, male_button_info
from app.keyboards.skip import *
from app.config import admin_id
import os
from app.keyboards.confirm.text import *
from app.handlers.commands import start
from app.keyboards.start import customer_start_keyboard
from app.keyboards.preliminary_calculation import preliminary_calculation_pdf_button_info, \
    preliminary_calculation_text_button_info
from app.services import incurance_property_storage, incurance_live_storage, incurance_live_and_property_storage
from app.keyboards.start.text import insurance_live_and_property_button_info, executed_documents_button_info


@bot.callback_query_handler(
    func=lambda call: insurance_live_and_property_button_info.filter(call.data) and incurance_live_storage.get_data(
        chat_id=call.message.chat.id, user_id=call.message.chat.id) == {}
                      and incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id,
                                                                       user_id=call.message.chat.id) == {}
                      and incurance_property_storage.get_data(chat_id=call.message.chat.id,
                                                              user_id=call.message.chat.id) == {})
def incurance_live_and_property0(call: CallbackQuery):
    incurance_live_and_property_storage.set_data(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                 key="1", value="1")
    incurance_live_and_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                  state="incurance_live_and_property")
    bot.send_message(chat_id=call.message.chat.id,
                     text='Укажите наименование банка, выдавшего ипотечный кредит')
    incurance_live_and_property_storage.set_data(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                 key="1", value="1")

    def set_incurance_live_and_property_bank(message: Message):
        incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                     key="bank", value=message.text)
        bot.send_message(chat_id=call.message.chat.id, text='Введите сумму кредита (остаток кредитной задолженности)')

        bot.register_next_step_handler(call.message, set_incurance_live_and_property_credit_balance)

    bot.register_next_step_handler(call.message, set_incurance_live_and_property_bank)

def set_incurance_live_and_property_credit_balance(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="credit_balance", value=message.text)
    bot.send_message(chat_id=message.chat.id, text='Введите дату рождения заемщика в формате ДД.ММ.ГГГГ')

    bot.register_next_step_handler(message, set_incurance_live_and_property_birthdate)

def set_incurance_live_and_property_birthdate(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="birthdate", value=message.text)
    bot.send_message(chat_id=message.chat.id, text="Выберите пол заемщика", reply_markup=choose_sex_keyboard)
    incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                  state="male")
    bot.callback_query_handler(choose_incurance_live_and_property_sex)

@bot.callback_query_handler(func=lambda call: male_button_info.filter(call.data) or
                                              female_button_info.filter(call.data) and
                                              incurance_live_and_property_storage.get_state(call.message.chat.id,
                                                                                            call.message.chat.id) == "male")
def choose_incurance_live_and_property_sex(call: CallbackQuery):

    incurance_live_and_property_storage.set_data(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                 key="sex",
                                                 value=call.data)
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Загрузите действующий полис \n(если нет действующего полиса "далее")',
                          reply_markup=skip_keyboard)
    incurance_live_and_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                  state="set_live_incurance_policy")

    def set_property_incurance_live_and_property_policy(message):
        (2)
        if incurance_live_and_property_storage.get_state(chat_id=call.message.chat.id,
                                                         user_id=call.message.chat.id) == "set_live_incurance_policy":
            if str(message.content_type) != "document" and str(message.content_type) != "photo":
                bot.send_message(chat_id=message.chat.id,
                                 text='Загрузите действующий полиc \n(если нет действующего полиса "далее")',
                                 reply_markup=skip_keyboard)

                bot.register_next_step_handler(message, set_property_incurance_live_and_property_policy)

            elif str(message.content_type) == "document":
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(message.document.file_name, 'wb') as f:
                    f.write(downloaded_file)

                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                    key=message.document.file_name,
                                    catalog="preliminary_calculation")
                bot.send_message(chat_id=message.chat.id, text='Данные отправлены менеджеру!')
                bot.send_message(chat_id=message.chat.id, text='Соcтавляем коммерческое предложение...')
                bot.send_message(chat_id=admin_id, text="Предварительный рассчёт\n"
                                                        "Страхование жизни и имущества\n"
                                                        f"<b>ID</b>: @{call.from_user.username}\n"
                                                        f"<b>Банк</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['bank']}\n"
                                                        f"<b>Сумма кредита</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['credit_balance']}\n"
                                                        f"<b>Дата рождения</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['birthdate']}\n"
                                                        f"<b>Пол</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['sex']}\n")
                mas = pdf.download_document(message.chat.id, "preliminary_calculation")

                if mas != None:
                    for i in mas:
                        try:
                            bot.send_document(admin_id, open(i, 'rb'))
                            os.remove(i)
                        except Exception as e:
                            (e)
                incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                              state="preliminary_calculation")
                preliminary_calculation_pdf_button = InlineKeyboardButton(
                    text=preliminary_calculation_pdf_button_info.text,
                    callback_data=preliminary_calculation_pdf_button_info.callback_data + f"[]{message.chat.id}")

                preliminary_calculation_text_button = InlineKeyboardButton(
                    text=preliminary_calculation_text_button_info.text,
                    callback_data=preliminary_calculation_text_button_info.callback_data + f"[]{message.chat.id}")
                preliminary_calculation_keyboard = InlineKeyboardMarkup()
                preliminary_calculation_keyboard.row(preliminary_calculation_text_button)
                preliminary_calculation_keyboard.row(preliminary_calculation_pdf_button)
                bot.send_message(chat_id=admin_id, text='Отправить коммерческое предложение',
                                 reply_markup=preliminary_calculation_keyboard)
            elif str(message.content_type) == "photo":
                i = 0
                for file in message.photo:
                    fileID = file.file_id
                    file_info = bot.get_file(fileID)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(file_info.file_path.split("/")[1], "wb") as f:
                        f.write(downloaded_file)
                        pdf = PDF()
                        pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                            key=f"incurance_policy{i}{file_info.file_path[-4:]}",
                                            catalog="preliminary_calculation")
                    i += 1
                bot.send_message(chat_id=message.chat.id, text='Данные отправлены менеджеру!')
                bot.send_message(chat_id=message.chat.id, text='Соcтавляем коммерческое предложение...')
                bot.send_message(chat_id=admin_id, text="Предварительный рассчёт\n"
                                                        "Страхование жизни и имущества\n"
                                                        f"<b>ID</b>: @{call.from_user.username}\n"
                                                        f"<b>Банк</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['bank']}\n"
                                                        f"<b>Сумма кредита</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['credit_balance']}\n"
                                                        f"<b>Дата рождения</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['birthdate']}\n"
                                                        f"<b>Пол</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['sex']}\n")
                mas = pdf.download_document(message.chat.id, "preliminary_calculation")

                if mas != None:
                    for i in mas:
                        try:
                            bot.send_document(admin_id, open(i, 'rb'))
                            os.remove(i)
                        except Exception as e:
                            (e)
                incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                              state="preliminary_calculation")
                preliminary_calculation_pdf_button = InlineKeyboardButton(
                    text=preliminary_calculation_pdf_button_info.text,
                    callback_data=preliminary_calculation_pdf_button_info.callback_data + f"[]{message.chat.id}")

                preliminary_calculation_text_button = InlineKeyboardButton(
                    text=preliminary_calculation_text_button_info.text,
                    callback_data=preliminary_calculation_text_button_info.callback_data + f"[]{message.chat.id}")
                preliminary_calculation_keyboard = InlineKeyboardMarkup()
                preliminary_calculation_keyboard.row(preliminary_calculation_text_button)
                preliminary_calculation_keyboard.row(preliminary_calculation_pdf_button)
                bot.send_message(chat_id=admin_id, text='Отправить коммерческое предложение',
                                 reply_markup=preliminary_calculation_keyboard)


        else:
            pass

    if incurance_live_and_property_storage.get_state(chat_id=call.message.chat.id,
                                                     user_id=call.message.chat.id) == "set_live_incurance_policy":
        bot.register_next_step_handler(call.message, set_property_incurance_live_and_property_policy)

@bot.callback_query_handler(
    func=lambda call: skip_button_info.filter(call.data) and incurance_live_and_property_storage.get_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id) == "set_live_incurance_policy")
def skip_incurance_live_and_property_policy(call: CallbackQuery):
    (99)
    bot.send_message(chat_id=call.message.chat.id, text='Данные отправлены менеджеру!')
    bot.send_message(chat_id=call.message.chat.id, text='Соcтавляем коммерческое предложение...')
    bot.send_message(chat_id=admin_id, text="Предварительный рассчёт\n"
                                            "Страхование жизни и имущества\n"
                                            f"<b>ID</b>: @{call.from_user.username}\n"
                                            f"<b>Банк</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['bank']}\n"
                                            f"<b>Сумма кредита</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['credit_balance']}\n"
                                            f"<b>Дата рождения</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['birthdate']}\n"
                                            f"<b>Пол</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['sex']}\n")

    incurance_live_and_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                  state="preliminary_calculation")

    preliminary_calculation_pdf_button = InlineKeyboardButton(
        text=preliminary_calculation_pdf_button_info.text,
        callback_data=preliminary_calculation_pdf_button_info.callback_data + f"[]{call.message.chat.id}")

    preliminary_calculation_text_button = InlineKeyboardButton(
        text=preliminary_calculation_text_button_info.text,
        callback_data=preliminary_calculation_text_button_info.callback_data + f"[]{call.message.chat.id}")
    preliminary_calculation_keyboard = InlineKeyboardMarkup()
    preliminary_calculation_keyboard.row(preliminary_calculation_text_button)
    preliminary_calculation_keyboard.row(preliminary_calculation_pdf_button)
    bot.send_message(chat_id=admin_id, text='Отправить коммерческое предложение',
                     reply_markup=preliminary_calculation_keyboard)

    bot.clear_step_handler_by_chat_id(call.message.chat.id)

    bot.callback_query_handler(get_text_or_pdf_preliminary_calculation_incurance_live_and_property)

@bot.callback_query_handler(
    func=lambda call:(call.data.split("[]")[0] == "text" or call.data.split("[]")[
        0] == "pdf") and  incurance_live_and_property_storage.get_state(int(call.data.split("[]")[1]), int(call.data.split("[]")[1]))
                                         =="preliminary_calculation" )
def get_text_or_pdf_preliminary_calculation_incurance_live_and_property(call: CallbackQuery):

    if call.data.split("[]")[0] == "text":
        incurance_live_and_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                      state="text_or_pdf")

        tg_id = int(call.data.split("[]")[1])
        bot.send_message(chat_id=admin_id, text='Напишите коммерческое предложение')

        def send_text_preliminary_calculation_lp(message: Message):
            preliminary_calculation_confirm_button = InlineKeyboardButton(
                text=preliminary_calculation_confirm_button_info.text,
                callback_data=preliminary_calculation_confirm_button_info.callback_data + f"[]{tg_id}")

            preliminary_calculation_reject_button = InlineKeyboardButton(
                text=preliminary_calculation_reject_button_info.text,
                callback_data=preliminary_calculation_reject_button_info.callback_data + f"[]{tg_id}")
            confirm_keyboard1 = InlineKeyboardMarkup()
            confirm_keyboard1.row(preliminary_calculation_confirm_button)
            confirm_keyboard1.row(preliminary_calculation_reject_button)
            bot.send_message(chat_id=tg_id,
                             text="Ваше коммерческое предложение:\n"
                                  f"{message.text}", reply_markup=confirm_keyboard1)
            incurance_live_and_property_storage.set_state(chat_id=tg_id, user_id=tg_id,
                                                          state="confirm")
            bot.callback_query_handler(set_reject_or_confirm_incurance_live_and_property)

        bot.register_next_step_handler(call.message, send_text_preliminary_calculation_lp)
    else:
        incurance_live_and_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                      state="text_or_pdf")
        tg_id = int(call.data.split("[]")[1])

        bot.send_message(chat_id=admin_id, text='Загрузите документ/фото')

        def send_pdf_preliminary_calculation_incurance_live_and_property(message: Message):
            if incurance_live_and_property_storage.get_state(int(call.data.split("[]")[1]), int(call.data.split("[]")[1]))=="preliminary_calculation":

                tg_id = int(call.data.split("[]")[1])
                if message.content_type != "document" and message.content_type!= "photo":
                    bot.send_message(chat_id=admin_id,
                                     text='Загрузите документ/фото')
                    bot.register_next_step_handler(call.message, send_pdf_preliminary_calculation_incurance_live_and_property)


                elif message.content_type == "document":
                    preliminary_calculation_confirm_button = InlineKeyboardButton(
                        text=preliminary_calculation_confirm_button_info.text,
                        callback_data=preliminary_calculation_confirm_button_info.callback_data + f"[]{tg_id}")

                    preliminary_calculation_reject_button = InlineKeyboardButton(
                        text=preliminary_calculation_reject_button_info.text,
                        callback_data=preliminary_calculation_reject_button_info.callback_data + f"[]{tg_id}")
                    confirm_keyboard = InlineKeyboardMarkup()
                    confirm_keyboard.row(preliminary_calculation_confirm_button)
                    confirm_keyboard.row(preliminary_calculation_reject_button)
                    file_info = bot.get_file(message.document.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(message.document.file_name, 'wb') as file:
                        file.write(downloaded_file)


                        bot.send_message(chat_id=tg_id,
                                         text="Ваше коммерческое предложение")
                        bot.send_document(tg_id, open(message.document.file_name, 'rb'),
                                          reply_markup=confirm_keyboard)
                        incurance_live_and_property_storage.set_state(chat_id=tg_id, user_id=tg_id,
                                                                      state="confirm")
                        bot.callback_query_handler(set_reject_or_confirm_incurance_live_and_property)
                elif message.content_type == "photo":
                    preliminary_calculation_confirm_button = InlineKeyboardButton(
                        text=preliminary_calculation_confirm_button_info.text,
                        callback_data=preliminary_calculation_confirm_button_info.callback_data + f"[]{tg_id}")

                    preliminary_calculation_reject_button = InlineKeyboardButton(
                        text=preliminary_calculation_reject_button_info.text,
                        callback_data=preliminary_calculation_reject_button_info.callback_data + f"[]{tg_id}")
                    confirm_keyboard = InlineKeyboardMarkup()
                    confirm_keyboard.row(preliminary_calculation_confirm_button)
                    confirm_keyboard.row(preliminary_calculation_reject_button)
                    fileID = message.photo[-1].file_id
                    file_info = bot.get_file(fileID)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(file_info.file_path.split("/")[1], "wb") as f:
                        f.write(downloaded_file)
                        try:
                            bot.send_message(chat_id=tg_id,
                                             text="Ваше коммерческое предложение")
                            bot.send_photo(tg_id, open(file_info.file_path.split("/")[1], 'rb'),
                                           reply_markup=confirm_keyboard)
                            os.remove(file_info.file_path.split("/")[1])

                        except Exception as e:
                            ((e))

                    incurance_live_and_property_storage.set_state(chat_id=tg_id, user_id=tg_id,
                                                                              state="confirm")
                    bot.callback_query_handler(set_reject_or_confirm_incurance_live_and_property)


        bot.register_next_step_handler(call.message, send_pdf_preliminary_calculation_incurance_live_and_property)

@bot.callback_query_handler(
    func=lambda call: (call.data.split("[]")[0] == "reject" or call.data.split("[]")[
        0] == "confirm") and incurance_live_and_property_storage.get_state(int(call.data.split("[]")[1]),
                                                                           int(call.data.split("[]")[1]))
                      == "confirm")
def set_reject_or_confirm_incurance_live_and_property(call: CallbackQuery):
    (call.data)
    (incurance_live_and_property_storage.get_state(chat_id=call.message.chat.id,
                                                   user_id=call.message.chat.id))
    if call.data.split("[]")[0] == "reject":

        bot.send_message(chat_id=admin_id, text=f"@{call.from_user.username} отклонил предложение")
        bot.send_message(chat_id=int(call.data.split("[]")[1]), text='Предложение отклонено')

        pdf = PDF()
        pdf.delete_from_ctalog(telegram_id=int(call.data.split("[]")[1]), catalog="preliminary_calculation")
        incurance_live_and_property_storage.set_state(chat_id=int(call.data.split("[]")[1]), user_id=int(call.data.split("[]")[1]),
                                         state="incurance_live_and_property")
        bot.clear_step_handler_by_chat_id(int(call.data.split("[]")[1]))

        incurance_live_and_property_storage.reset_data(int(call.data.split("[]")[1]), int(call.data.split("[]")[1]))

        bot.send_message(chat_id=int(call.data.split("[]")[1]),
                         text='Главное меню',
                         reply_markup=customer_start_keyboard)


    else:
        if  incurance_live_and_property_storage.get_state(int(call.data.split("[]")[1]),
                                                                           int(call.data.split("[]")[1]))== "confirm":
            bot.send_message(chat_id=admin_id,
                             text=f"@{call.from_user.username} подтвердил коммерческое предложение")
            incurance_live_and_property_storage.set_state(chat_id=int(call.data.split("[]")[1]),
                                                          user_id=int(call.data.split("[]")[1]),
                                                          state="incurance_live_and_property_policy")

            bot.send_message(int(call.data.split("[]")[1]),
                             text='Отлично! Теперь введите дату начала действия полиса в формате ДД.ММ.ГГГГ')

        def set_policy_start_date_incurance_live_and_property(message: Message):
            incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                         key="policy_start_date", value=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text='Введите процентную ставку по кредиту')

            bot.register_next_step_handler(message, set_interest_rate_incurance_live_and_property)

        bot.register_next_step_handler(call.message, set_policy_start_date_incurance_live_and_property)

def set_interest_rate_incurance_live_and_property(message: Message):
    incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                  state="incurance_live_and_property_policy")

    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="interest_rate", value=message.text)
    bot.send_message(chat_id=message.chat.id, text='Введите номер кредитного договора')

    bot.register_next_step_handler(message, set_contract_number_incurance_live_and_property)

def set_contract_number_incurance_live_and_property(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="contract_number", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Введите дату подписания кредитного договора в формате ДД.ММ.ГГГГ")
    bot.register_next_step_handler(message, set_contract_sign_date_incurance_live_and_property)

def set_contract_sign_date_incurance_live_and_property(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="contract_sign_date", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Введите дату окончания кредитного договора в формате ДД.ММ.ГГГГ")
    bot.register_next_step_handler(message, set_contract_end_date_incurance_live_and_property)

def set_contract_end_date_incurance_live_and_property(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="contract_end_date", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Введите ФИО")
    (incurance_live_and_property_storage.get_state(chat_id=message.chat.id, user_id=message.chat.id))

    bot.register_next_step_handler(message, set_contract_initials_incurance_live_and_property)

def set_contract_initials_incurance_live_and_property(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="contract_initials", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Загрузите скан/фото паспорта (первая страница)")
    bot.register_next_step_handler(message, set_first_pasport_incurance_live_and_property)

def set_first_pasport_incurance_live_and_property(message: Message):
    if message.content_type != "photo" and message.content_type != "document":
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите скан/фото паспорта (первая страница)")
        bot.register_next_step_handler(message, set_first_pasport_incurance_live_and_property)
    elif message.content_type == "photo":
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_info.file_path.split("/")[1], "wb") as f:
            f.write(downloaded_file)
            pdf = PDF()
            pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                key=f"Passport1{file_info.file_path[-4:]}",
                                catalog="policy")
        try:
            os.remove(file_info.file_path.split("/")[1])
        except Exception as e:
            (e)
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите скан/фото паспорта (адрес регистрации)")

        bot.register_next_step_handler(message, set_registration_pasport_incurance_live_and_property)
    elif message.content_type == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as f:
            f.write(downloaded_file)

        pdf = PDF()
        pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                            key=message.document.file_name,
                            catalog="policy")
        try:
            os.remove(file_info.file_path.split("/")[1])
        except Exception as e:
            (e)
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите фото паспорта (адрес регистрации)")

        bot.register_next_step_handler(message, set_registration_pasport_incurance_live_and_property)
def set_registration_pasport_incurance_live_and_property(message: Message):
    if message.content_type != "photo" and message.content_type!= "document":
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите фото паспорта (адрес регистрации)")

        bot.register_next_step_handler(message, set_registration_pasport_incurance_live_and_property)
    elif message.content_type == "photo":
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_info.file_path.split("/")[1], "wb") as f:
            f.write(downloaded_file)
            pdf = PDF()
            pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                key="Passport2" + file_info.file_path[-4:],
                                catalog="policy")
        try:
            os.remove(file_info.file_path.split("/")[1])
        except Exception as e:
            (e)
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите все страницы кредитного договора.")

        bot.register_next_step_handler(message, set_loan_agreement_lp)
    elif message.content_type == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as f:
            f.write(downloaded_file)

        pdf = PDF()
        pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                            key=message.document.file_name,
                            catalog="policy")
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите все страницы кредитного договора.")

        bot.register_next_step_handler(message, set_loan_agreement_lp)

def set_loan_agreement_lp(message: Message):

    if str(message.content_type) == "photo":
        i = 0
        for file in message.photo:
            fileID = file.file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_info.file_path.split("/")[1], "wb") as f:
                f.write(downloaded_file)
                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                    key=f"loan_agreement{i}{file_info.file_path[-4:]}",
                                    catalog="policy")
            i += 1
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите выписку ЕГРН")
        bot.register_next_step_handler(message, set_property_EGRN_lp)
    elif str(message.content_type) == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as f:
            f.write(downloaded_file)

        pdf = PDF()
        pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                            key=message.document.file_name,
                            catalog="policy")
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите выписку ЕГРН")
        bot.register_next_step_handler(message, set_property_EGRN_lp)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите все страницы кредитного договора.")

        bot.register_next_step_handler(message, set_loan_agreement_lp)

def set_property_EGRN_lp(message: Message):
    if str(message.content_type) == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        (message.document.file_name)
        with open(message.document.file_name, 'wb') as f:
            f.write(downloaded_file)

        pdf = PDF()
        pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                            key='ЕГРН',
                            catalog="policy")
        try:
            os.remove(message.document.file_name)
        except Exception as e:
            (e)
        bot.send_message(chat_id=message.chat.id,
                         text="Супер! Теперь введите ваш рост в см")
        bot.register_next_step_handler(message, set_heigh_lp)
    elif(message.content_type) == "photo":
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_info.file_path.split("/")[1], "wb") as f:
            f.write(downloaded_file)
            pdf = PDF()
            pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                key="ЕГРН" + file_info.file_path[-4:],
                                catalog="policy")
        try:
            os.remove(file_info.file_path.split("/")[1])
        except Exception as e:
            (e)
        bot.send_message(chat_id=message.chat.id,
                         text="Супер! Теперь введите ваш рост в см")
        bot.register_next_step_handler(message, set_heigh_lp)
    elif message.content_type != "photo" and message.content_type!="document":
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите выписку ЕГРН")
        bot.register_next_step_handler(message, set_property_EGRN_lp)


def set_heigh_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="height", value=message.text)
    bot.send_message(chat_id=message.chat.id, text='Вес в кг')

    bot.register_next_step_handler(message, set_weight_lp)

def set_weight_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="weight", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Верхнее и нижнее давление")
    bot.register_next_step_handler(message, set_upper_and_lower_pressure_lp)

def set_upper_and_lower_pressure_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="upper_and_lower_pressure", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Пожалуйста введите ваше место работы",
                     reply_markup=telebot.types.ReplyKeyboardRemove(None))
    bot.register_next_step_handler(message, set_workplace_lp)

def set_workplace_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="workplace", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Введите должность", reply_markup=telebot.types.ReplyKeyboardRemove(None))
    bot.register_next_step_handler(message, set_position_lp)

def set_position_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="position", value=message.text)

    bot.send_message(chat_id=message.chat.id,
                     text="Профессию")
    bot.register_next_step_handler(message, set_profesion_lp)

def set_profesion_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="profession", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Отлично! Теперь введите адрес обьекта регистрации")
    bot.register_next_step_handler(message, set_address_insurance_live_and_property)

def set_address_insurance_live_and_property(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="address_insurance", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Площадь квартиры")
    bot.register_next_step_handler(message, set_address_area_lp)

def set_address_area_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="address_area", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Количество этажей в подъезде")
    bot.register_next_step_handler(message, set_floor_number_lp)

def set_floor_number_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="floor_number", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Ваш этаж")
    bot.register_next_step_handler(message, set_floor_lp)

def set_floor_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="floor", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Пожалуйста введите год постройки дома")
    bot.register_next_step_handler(message, set_year_construction_lp)

def set_year_construction_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="year_construction", value=message.text)
    bot.send_message(chat_id=message.chat.id,
                     text="Необходимо поделиться номером телефона", reply_markup=share_contact_keyboard)
    bot.register_next_step_handler(message, set_phone_number_lp)

def set_phone_number_lp(message: Message):
    if message.content_type != "contact":
        bot.send_message(chat_id=message.chat.id,
                         text="Необходимо поделиться номером телефона", reply_markup=share_contact_keyboard)
        bot.register_next_step_handler(message, set_phone_number_lp)
    else:
        f = open("users.txt", "a")
        a=bot.get_chat_member(message.chat.id,message.chat.id)
        f.write(
            f"{message.chat.id}[]{a.user.username}[]@{a.user.username}[]{message.contact.phone_number}\n")
        f.close()
        incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                     key="phone_number", value=message.contact.phone_number)
        bot.send_message(chat_id=message.chat.id,
                         text='Адрес электронной почты', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, set_email_lp)

def set_email_lp(message: Message):
    incurance_live_and_property_storage.set_data(chat_id=message.chat.id, user_id=message.chat.id,
                                                 key="email", value=message.text)

    def property_load_policy_lp(message: Message):

        if incurance_live_and_property_storage.get_state(chat_id=message.chat.id,
                                                         user_id=message.chat.id) == "set_live_incurance_load_policy":
            if message.content_type != "document"and message.content_type != "photo":
                bot.send_message(chat_id=message.chat.id,
                                 text='Загрузите действующий полис  \n(если оформляете новый, то "далее")',
                                 reply_markup=skip_keyboard)
                bot.register_next_step_handler(message, property_load_policy_lp)

            elif message.content_type == "document":
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(message.document.file_name, 'wb') as f:
                    f.write(downloaded_file)

                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                    key=message.document.file_name,
                                    catalog="policy")
                paymant_button = InlineKeyboardButton(text='Отправить ссылку для оплаты...',
                                                      callback_data=f"paymant[]{message.chat.id}")

                paymant_keyboard = InlineKeyboardMarkup()
                paymant_keyboard.row(paymant_button)
                bot.send_message(chat_id=message.chat.id, text='Данные отправлены менеджеру!')
                bot.send_message(chat_id=message.chat.id, text='Пожалуйста, ожидайте ссылку на оплату')
                bot.send_message(chat_id=admin_id, text="Оформление полиса\n"
                                                        "Страхование имущества\n"
                                                        f"<b>ID</b>: @{message.from_user.username}\n"
                                                        f"<b>Банк</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['bank']}\n"
                                                        f"<b>Сумма кредита</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['credit_balance']}\n"
                                                        f"<b>Дата рождения</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['birthdate']}\n"
                                                        f"<b>Пол</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['sex']}\n"
                                                        f"<b>Дата начала действия полиса</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['policy_start_date']}\n"
                                                        f"<b>Процентная ставка по кредиту</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['interest_rate']}\n"
                                                        f"<b>Номер кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_number']}\n"
                                                        f"<b>Дата подписания кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_sign_date']}\n"
                                                        f"<b>Дата окончания кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_end_date']}\n"
                                                        f"<b>ФИО заемщика</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_initials']}\n"
                                                        f"<b>Рост</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['height']}\n"
                                                        f"<b>Вес</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['weight']}\n"
                                                        f"<b>Верхнее и нижнее давление</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['upper_and_lower_pressure']}\n"
                                                        f"<b>Профессия</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['workplace']}\n"
                                                        f"<b>Место работы</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['position']}\n"
                                                        f"<b>Должность</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['profession']}\n"
                                                        f"<b>Адрес объекта страхования </b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['address_insurance']}\n"
                                                        f"<b>Площадь квартиры</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['address_area']}\n"
                                                        f"<b>Этаж</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['floor']}\n"
                                                        f"<b>Количество этажей в подъезде </b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['floor_number']}\n"
                                                        f"<b>Адрес электронной почты</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['email']}\n"
                                                        f"<b>Номер телефона</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['phone_number']}\n"
                                                        f"<b>Год постройки дома</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['year_construction']}\n",
                                 reply_markup=paymant_keyboard)

                mas = pdf.download_document(message.chat.id, "policy")
                a = pdf.download_document(message.chat.id, "preliminary_calculation")
                if mas != None:
                    if a != None:
                        mas += a
                if mas != None:
                    for i in mas:
                        if i[-4:] in [".jpg", ".png", ".jpeg", ".bmp"]:
                            for j in [".jpg", ".png", ".jpeg", ".bmp"]:
                                if i[-4:] == j:
                                    try:
                                        bot.send_photo(admin_id, open(i, 'rb'))
                                        os.remove(i)

                                    except Exception as e:
                                        (e)
                        else:
                            try:
                                bot.send_document(admin_id, open(i, 'rb'))
                                os.remove(i)

                            except Exception as e:
                                (e)
                incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                              state="waiting_confirm_live")
                pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="preliminary_calculation")
                pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="policy")
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
                incurance_live_and_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
                bot.send_message(chat_id=message.chat.id,
                                 text='Главное меню',
                                 reply_markup=customer_start_keyboard)
            elif message.content_type == "photo":
                fileID = message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(file_info.file_path.split("/")[1], "wb") as f:
                    f.write(downloaded_file)
                    pdf = PDF()
                    pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                        key="incurance_policy" + file_info.file_path[-4:],
                                        catalog="policy")
                try:
                    os.remove(file_info.file_path.split("/")[1])
                except Exception as e:
                    (e)
                paymant_button = InlineKeyboardButton(text='Отправить ссылку для оплаты...',
                                                      callback_data=f"paymant[]{message.chat.id}")

                paymant_keyboard = InlineKeyboardMarkup()
                paymant_keyboard.row(paymant_button)
                bot.send_message(chat_id=message.chat.id, text='Данные отправлены менеджеру!')
                bot.send_message(chat_id=message.chat.id, text='Пожалуйста, ожидайте ссылку на оплату')
                bot.send_message(chat_id=admin_id, text="Оформление полиса\n"
                                                        "Страхование имущества\n"
                                                        f"<b>ID</b>: @{message.from_user.username}\n"
                                                        f"<b>Банк</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['bank']}\n"
                                                        f"<b>Сумма кредита</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['credit_balance']}\n"
                                                        f"<b>Дата рождения</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['birthdate']}\n"
                                                        f"<b>Пол</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['sex']}\n"
                                                        f"<b>Дата начала действия полиса</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['policy_start_date']}\n"
                                                        f"<b>Процентная ставка по кредиту</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['interest_rate']}\n"
                                                        f"<b>Номер кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_number']}\n"
                                                        f"<b>Дата подписания кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_sign_date']}\n"
                                                        f"<b>Дата окончания кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_end_date']}\n"
                                                        f"<b>ФИО заемщика</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['contract_initials']}\n"
                                                        f"<b>Рост</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['height']}\n"
                                                        f"<b>Вес</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['weight']}\n"
                                                        f"<b>Верхнее и нижнее давление</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['upper_and_lower_pressure']}\n"
                                                        f"<b>Профессия</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['workplace']}\n"
                                                        f"<b>Место работы</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['position']}\n"
                                                        f"<b>Должность</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['profession']}\n"
                                                        f"<b>Адрес объекта страхования </b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['address_insurance']}\n"
                                                        f"<b>Площадь квартиры</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['address_area']}\n"
                                                        f"<b>Этаж</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['floor']}\n"
                                                        f"<b>Количество этажей в подъезде </b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['floor_number']}\n"
                                                        f"<b>Адрес электронной почты</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['email']}\n"
                                                        f"<b>Номер телефона</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['phone_number']}\n"
                                                        f"<b>Год постройки дома</b>: {incurance_live_and_property_storage.get_data(chat_id=message.chat.id, user_id=message.chat.id)['year_construction']}\n",
                                 reply_markup=paymant_keyboard)

                mas = pdf.download_document(message.chat.id, "policy")
                a = pdf.download_document(message.chat.id, "preliminary_calculation")
                if mas != None:
                    if a != None:
                        mas += a
                if mas != None:
                    for i in mas:
                        if i[-4:] in [".jpg", ".png", ".jpeg", ".bmp"]:
                            for j in [".jpg", ".png", ".jpeg", ".bmp"]:
                                if i[-4:] == j:
                                    try:
                                        bot.send_photo(admin_id, open(i, 'rb'))
                                        os.remove(i)

                                    except Exception as e:
                                        (e)
                        else:
                            try:
                                bot.send_document(admin_id, open(i, 'rb'))
                                os.remove(i)

                            except Exception as e:
                                (e)
                incurance_live_and_property_storage.set_state(chat_id=message.chat.id, user_id=message.chat.id,
                                                              state="waiting_confirm_live")
                pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="preliminary_calculation")
                pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="policy")
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
                incurance_live_and_property_storage.reset_data(chat_id=message.chat.id, user_id=message.chat.id)
                bot.send_message(chat_id=message.chat.id,
                                 text='Главное меню',
                                 reply_markup=customer_start_keyboard)
        else:
            pass

    if incurance_live_and_property_storage.get_state(chat_id=message.chat.id,
                                                     user_id=message.chat.id) == "incurance_live_and_property_policy":
        incurance_live_and_property_storage.set_state(chat_id=message.chat.id,
                                                      user_id=message.chat.id,
                                                      state="set_live_incurance_load_policy")
        bot.register_next_step_handler(message, property_load_policy_lp)
        bot.callback_query_handler(load_policy_skip_lp)

        bot.send_message(chat_id=message.chat.id,
                         text='Загрузите действующий полис \n(если оформляете новый, то "далее")',
                         reply_markup=skip_keyboard)

@bot.callback_query_handler(
    func=lambda call: skip_button_info.filter(call.data) and incurance_live_and_property_storage.get_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id) == "set_live_incurance_load_policy"
    )
def load_policy_skip_lp(call: CallbackQuery):
    paymant_button = InlineKeyboardButton(text='Отправить ссылку для оплаты...',
                                          callback_data=f"paymant[]{call.message.chat.id}")

    paymant_keyboard = InlineKeyboardMarkup()
    paymant_keyboard.row(paymant_button)
    bot.send_message(chat_id=call.message.chat.id, text='Данные отправлены менеджеру!')
    bot.send_message(chat_id=call.message.chat.id, text='Пожалуйста, ожидайте ссылку на оплату')
    bot.send_message(chat_id=admin_id, text="Оформление полиса\n"
                                            "Страхование жизни и имущества\n"
                                            f"<b>ID</b>: @{call.message.from_user.username}\n"
                                            f"<b>Банк</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['bank']}\n"
                                            f"<b>Сумма кредита</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['credit_balance']}\n"
                                            f"<b>Дата рождения</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['birthdate']}\n"
                                            f"<b>Пол</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['sex']}\n"
                                            f"<b>Дата начала действия полиса</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['policy_start_date']}\n"
                                            f"<b>Процентная ставка по кредиту</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['interest_rate']}\n"
                                            f"<b>Номер кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_number']}\n"
                                            f"<b>Дата подписания кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_sign_date']}\n"
                                            f"<b>Дата окончания кредитного договора</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_end_date']}\n"
                                            f"<b>ФИО заемщика</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_initials']}\n"
                                            f"<b>Рост</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['height']}\n"
                                            f"<b>Вес</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['weight']}\n"
                                            f"<b>Верхнее и нижнее давление</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['upper_and_lower_pressure']}\n"
                                            f"<b>Адрес электронной почты</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['email']}\n"
                                            f"<b>Номер телефона</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['phone_number']}\n"
                                            f"<b>Профессия</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['workplace']}\n"
                                            f"<b>Место работы</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['position']}\n"
                                            f"<b>Должность</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['profession']}\n"

                                            f"<b>Адрес объекта страхования </b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['address_insurance']}\n"
                                            f"<b>Площадь квартиры</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['address_area']}\n"
                                            f"<b>Этаж</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['floor']}\n"
                                            f"<b>Количество этажей в подъезде </b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['floor_number']}\n"
                                            f"<b>Адрес электронной почты</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['email']}\n"
                                            f"<b>Номер телефона</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['phone_number']}\n"
                                            f"<b>Год постройки дома</b>: {incurance_live_and_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['year_construction']}\n",
                     reply_markup=paymant_keyboard)
    incurance_live_and_property_storage.reset_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)

    pdf = PDF()
    mas = pdf.download_document(call.message.chat.id, "policy")
    a = pdf.download_document(call.message.chat.id, "preliminary_calculation")
    if mas != None:
        if a != None:
            mas += a

    if mas != None:

        for i in mas:
            if i[-4:] in [".jpg", ".png", ".jpeg", ".bmp"]:
                for j in [".jpg", ".png", ".jpeg", ".bmp"]:
                    if i[-4:] == j:
                        try:
                            bot.send_photo(admin_id, open(i, 'rb'))
                            os.remove(i)

                        except Exception as e:
                            (e)
            else:
                try:
                    bot.send_document(admin_id, open(i, 'rb'))
                    os.remove(i)

                except Exception as e:
                    (e)
    incurance_live_and_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.chat.id,
                                                  state="waiting_confirm_live")
    pdf.delete_from_ctalog(telegram_id=call.message.chat.id, catalog="preliminary_calculation")
    pdf.delete_from_ctalog(telegram_id=call.message.chat.id, catalog="policy")

    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    incurance_live_and_property_storage.reset_data(chat_id=call.message.chat.id,
                                            user_id=call.message.chat.id
                                            )
    bot.send_message(chat_id=call.message.chat.id,
                     text='Главное меню',
                     reply_markup=customer_start_keyboard)
@bot.callback_query_handler(
    func=lambda call: call.data.split("[]")[0] == "paymant" and str(call.message.chat.id) == admin_id)
def confirm_paymant_property_lp(call: CallbackQuery):

    bot.send_message(admin_id,
                     text='Отправьте ссылку для оплаты')
    tg_id = int(call.data.split("[]")[1])

    def send_documents_lp(message: Message):
        bot.send_message(chat_id=tg_id,
                         text="Ссылка для оплаты полиса:"
                              f"{message.text}")



    bot.register_next_step_handler(admin_id, send_documents_lp)
