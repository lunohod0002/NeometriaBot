import telebot.types
from app.keyboards.helpers import share_contact_keyboard
from app import bot
from app.API.PDF import PDF
from telebot.types import CallbackQuery, Message
from app.keyboards.sex import choose_sex_keyboard, female_button_info, male_button_info
from app.keyboards.skip import *
from app.config import admin_id
from app.keyboards.confirm import *
import os
from app.keyboards.preliminary_calculation import preliminary_calculation_pdf_button_info, \
    preliminary_calculation_text_button_info
from app.services import incurance_live_storage
from app.keyboards.start.text import insurance_live_button_info, executed_documents_button_info


@bot.callback_query_handler(func=lambda call: insurance_live_button_info.filter(call.data))
def incurance_live(call: CallbackQuery):
    incurance_live_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state="incurance_live")
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Укажите наименование банка, выдавшего ипотечный кредит')

    def set_incurance_live_bank(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="bank", value=message.text)
        bot.send_message(chat_id=call.message.chat.id, text='Введите сумму кредита (остаток кредитной задолженности')

        bot.register_next_step_handler(call.message, set_incurance_live_credit_balance)

    bot.register_next_step_handler(call.message, set_incurance_live_bank)


def set_incurance_live_credit_balance(message: Message):
    incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                    key="credit_balance", value=message.text)
    bot.send_message(chat_id=message.chat.id, text='Введите дату рождения заемщика в формате ДД.ММ.ГГГГ')

    bot.register_next_step_handler(message, set_incurance_live_birthdate)


def set_incurance_live_birthdate(message: Message):
    incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                    key="birthdate", value=message.text)
    bot.send_message(chat_id=message.chat.id, text="Выберите пол заемщика", reply_markup=choose_sex_keyboard)
    incurance_live_storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                    state="live_sex")

    @bot.callback_query_handler(func=lambda call: male_button_info.filter(call.data) or
                                                  female_button_info.filter(call.data) and
                                                  incurance_live_storage.get_state(call.message.chat.id,
                                                                                   call.from_user.id) == "live_sex")
    def choose_incurance_live_sex(call: CallbackQuery):
        incurance_live_storage.set_data(chat_id=call.message.chat.id, user_id=call.from_user.id, key="sex",
                                        value=call.data)
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Загрузите действующий полис в формате pdf \n(если нет действующего полиса "пропустить"',
                              reply_markup=skip_keyboard)


        def set_incurance_live_policy(message: Message):
            if message.content_type != "document":
                bot.send_message(chat_id=message.chat.id,
                                 text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "пропустить"',
                                 reply_markup=skip_keyboard)
                bot.register_next_step_handler(call.message, set_incurance_live_policy)

            else:
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                print(message.document.file_name)
                with open(message.document.file_name, 'wb') as f:
                    f.write(downloaded_file)

                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                        key=message.document.file_name,
                                        catalog="preliminary_calculation")
                bot.send_message(chat_id=message.chat.id, text='Данные отправлены менеджеру!')
                bot.send_message(chat_id=message.chat.id, text='Соcтавляем коммерческое предложение...')
                bot.send_message(chat_id=admin_id, text="Предварительный рассчёт\n"
                                                        "Страхование жизни\n"
                                                        f"<b>ID</b>: @{call.from_user.username}\n"
                                                        f"<b>Банк</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['bank']}\n"
                                                        f"<b>Сумма кредита</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['credit_balance']}\n"
                                                        f"<b>Дата рождения</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['birthdate']}\n"
                                                        f"<b>Пол</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['sex']}\n")
                mas = pdf.download_document(message.chat.id, "preliminary_calculation")
                if mas != None:
                    for i in mas:
                        bot.send_document(admin_id, open(i, 'rb'))
                        os.remove(i)
                incurance_live_storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
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
                incurance_live_storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                                state="live_pdf_or_txt")

        bot.register_next_step_handler(call.message, set_incurance_live_policy)




    @bot.callback_query_handler(
        func=lambda call: call.data.split("[]")[0] == "text" and incurance_live_storage.get_state(chat_id=call.message.chat.id, user_id=call.from_user.id)=="live_pdf_or_txt")
    def get_text_preliminary_calculation(call: CallbackQuery):
        incurance_live_storage.set_state(call.message.chat.id,
                                         call.from_user.id, state="incurance_lives")
        tg_id = call.data.split("[]")[1]
        incurance_live_storage.set_state(tg_id, tg_id, state="preliminary_calculation_policy")
        bot.send_message(chat_id=admin_id, text='Напишите коммерческое предложение')

        def send_text_preliminary_calculation(message: Message):
            tg_id = call.data.split("[]")[1]
            bot.send_message(chat_id=tg_id,
                             text="Ваше коммерческое предложение:\n"
                                  f"{message.text}", reply_markup=confirm_keyboard)

        bot.register_next_step_handler(call.message, send_text_preliminary_calculation)


    @bot.callback_query_handler(
        func=lambda call: call.data.split("[]")[0] == "pdf" and incurance_live_storage.get_state(chat_id=call.message.chat.id, user_id=call.from_user.id)=="live_pdf_or_txt")
    def get_pdf_preliminary_calculation(call: CallbackQuery):
        incurance_live_storage.set_state(call.message.chat.id, call.from_user.id,
                                         state="incurance_lives")

        bot.send_message(chat_id=admin_id, text='Загрузите pdf документ')

        def send_pdf_preliminary_calculation(message: Message):
            tg_id = call.data.split("[]")[1]
            if message.content_type != "document":
                bot.send_message(chat_id=admin_id,
                                 text='Загрузите pdf документ')
                bot.register_next_step_handler(call.message, send_pdf_preliminary_calculation)

            else:
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(message.document.file_name, 'wb') as file:
                    file.write(downloaded_file)

                    pdf = PDF()

                    bot.send_message(chat_id=tg_id,
                                     text="Ваше коммерческое предложение:")
                    bot.send_document(tg_id, open(message.document.file_name, 'rb'),
                                      reply_markup=confirm_keyboard)

        bot.register_next_step_handler(call.message, send_pdf_preliminary_calculation)


    @bot.callback_query_handler(
        func=lambda call: call.data == "reject" and incurance_live_storage.get_state(chat_id=call.message.chat.id,
                                                                                     user_id=call.from_user.id) != "incurance_lives")
    def set_reject(call: CallbackQuery):
        bot.send_message(chat_id=admin_id, text=f"@{call.from_user.username} отклонил предложение")
        bot.send_message(chat_id=call.message.chat.id, text='Предложение отклонено')
        incurance_live_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                                         state="incurance_policy")


    @bot.callback_query_handler(
        func=lambda call: preliminary_calculation_confirm_button_info.filter(call.data)
    )
    def set_confirm(call: CallbackQuery):
        bot.send_message(chat_id=admin_id,
                         text=f"@{call.from_user.username} подтвердил коммерческое предложение")
        incurance_live_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                                         state="incurance_policy")

        bot.send_message(call.message.chat.id,
                         text='Отлично! Теперь введите дату начала действия полиса')

        def set_policy_start_date(message: Message):
            incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                            key="policy_start_date", value=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text='Введите процентную_ ставку по кредиту')

            bot.register_next_step_handler(message, set_interest_rate)

        bot.register_next_step_handler(call.message, set_policy_start_date)


    def set_interest_rate(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="interest_rate", value=message.text)
        bot.send_message(chat_id=message.chat.id, text='Введите номер кредитного договора')

        bot.register_next_step_handler(message, set_contract_number)


    def set_contract_number(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_number", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите дату подписания кредитного договора в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(message, set_contract_sign_date)


    def set_contract_sign_date(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_sign_date", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите дату окончания кредитного договора в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(message, set_contract_end_date)


    def set_contract_end_date(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_end_date", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите ФИО")
        bot.register_next_step_handler(message, set_contract_initials)


    def set_contract_initials(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_initials", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите фото паспорта (первая страница")
        bot.register_next_step_handler(message, set_first_pasport)


    def set_first_pasport(message: Message):
        if message.content_type != "photo":
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите фото паспорта (первая страница")
            bot.register_next_step_handler(message, set_first_pasport)
        else:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_info.file_path.split("/")[1], "wb") as f:
                f.write(downloaded_file)
                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                    key=f"Passport1{file_info.file_path[-4:]}",
                                    catalog="policy")

            os.remove(file_info.file_path.split("/")[1])
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите фото паспорта (адрес регистрации)")

            bot.register_next_step_handler(message, set_registration_pasport)


    def set_registration_pasport(message: Message):
        if message.content_type != "photo":
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите фото паспорта (адрес регистрации)")

            bot.register_next_step_handler(message, set_registration_pasport)
        else:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_info.file_path.split("/")[1], "wb") as f:
                f.write(downloaded_file)
                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                    key="Passport2"+file_info.file_path[-4:],
                                    catalog="policy")

            os.remove(file_info.file_path.split("/")[1])
            stop_keyboard = telebot.types.ReplyKeyboardMarkup()
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите все страницы кредитного договора.")

            bot.register_next_step_handler(message, set_loan_agreement)


    def set_loan_agreement(message: Message):
        print(message.content_type)

        if str(message.content_type) == "photo":
            i = 0
            for file in message.photo:
                i += 1
                fileID = file.file_id
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(file_info.file_path.split("/")[1], "wb") as f:
                    f.write(downloaded_file)
                    pdf = PDF()
                    pdf.upload_document(telegram_id=message.chat.id, file_name=file_info.file_path.split("/")[1],
                                        key=f"loan_agreement{i}{file_info.file_path[-4:]}",
                                        catalog="policy")
                os.remove(file_info.file_path.split("/")[1])
            bot.send_message(chat_id=message.chat.id,
                                 text="Супер! Теперь введите ваш рост")
            bot.register_next_step_handler(message, set_height)
        elif str(message.content_type) == "document":
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                print(message.document.file_name)
                with open(message.document.file_name, 'wb') as f:
                    f.write(downloaded_file)

                pdf = PDF()
                pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                    key=message.document.file_name,
                                    catalog="policy")
                os.remove(message.document.file_id)
                bot.send_message(chat_id=message.chat.id,
                                 text="Супер! Теперь введите ваш рост")
                bot.register_next_step_handler(message, set_height)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите все страницы кредитного договора.")

            bot.register_next_step_handler(message, set_loan_agreement)


    def set_height(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="height", value=message.text)
        bot.send_message(chat_id=message.chat.id, text='Вес:')

        bot.register_next_step_handler(message, set_weight)


    def set_weight(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="weight", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Верхнее и нижнее давление")
        bot.register_next_step_handler(message, set_upper_and_lower_pressure)


    def set_upper_and_lower_pressure(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="upper_and_lower_pressure", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Адрес электронный почты:")
        bot.register_next_step_handler(message, set_email)


    def set_email(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="email", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Необходимо поделиться номером телефона", reply_markup=share_contact_keyboard)
        bot.register_next_step_handler(message, set_phone_number)


    def set_phone_number(message: Message):
        if message.content_type!="contact":
            bot.send_message(chat_id=message.chat.id,
                             text="Необходимо поделиться номером телефона", reply_markup=share_contact_keyboard)
            bot.register_next_step_handler(message, set_phone_number)
        else:
            with open("users.txt","w+") as f:
                f.write(f"{message.chat.id}[]{message.from_user.username}[]@{message.from_user.username}[]{message.contact.phone_number}")
            incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                            key="phone_number", value=message.contact.phone_number)
            bot.send_message(chat_id=message.chat.id,
                             text="Пожалуйста введите ваше место работы")
            bot.register_next_step_handler(message, set_workplace)




    def set_workplace(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="workplace", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите должность:")
        bot.register_next_step_handler(message, set_position)


    def set_position(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="position", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Проффесию:")
        bot.register_next_step_handler(message, set_profesion)


    def set_profesion(message: Message):
        incurance_live_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="profession", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text='Загрузите предыдущий полис в фомрмате pdf \n(если оформляете новый то "пропустить"',
                         reply_markup=skip_keyboard)
        bot.register_next_step_handler(message, load_policy)
    def load_policy(message: Message):
        if message.content_type != "document":
            bot.send_message(chat_id=message.chat.id,
                             text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "пропустить"',
                             reply_markup=skip_keyboard)
            bot.register_next_step_handler(message, load_policy)

        else:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print(incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id))
            with open(message.document.file_name, 'wb') as f:
                f.write(downloaded_file)

            pdf = PDF()
            pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                key=message.document.file_name,
                                catalog="policy")
            paymant_button = InlineKeyboardButton(text='Отправить ссылку для оплаты...', callback_data=f"paymant[]{message.chat.id}")

            paymant_keyboard = InlineKeyboardMarkup()
            paymant_keyboard.row(paymant_button)
            bot.send_message(chat_id=message.chat.id, text='Данные отправлены менеджеру!')
            bot.send_message(chat_id=message.chat.id, text='Пожалуйста, ожидайте ссылку на оплату')
            bot.send_message(chat_id=admin_id, text="Оформление полиса\n"
                                                    "Страхование жизни\n"
                                                    f"<b>ID</b>: @{message.from_user.username}\n"
                                                    f"<b>Банк</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['bank']}\n"
                                                    f"<b>Сумма кредита</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['credit_balance']}\n"
                                                    f"<b>Дата рождения</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['birthdate']}\n"
                                                    f"<b>Пол</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['sex']}\n"
                                                    f"<b>Дата начала действия полиса</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['policy_start_date']}\n"
                                                    f"<b>Процентная ставка по кредиту</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['interest_rate']}\n"
                                                    f"<b>Номер кредитного договора</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_number']}\n"
                                                    f"<b>Дата подписания кредитного договора</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_sign_date']}\n"
                                                    f"<b>Дата окончания кредитного договора</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_end_date']}\n"
                                                    f"<b>ФИО заемщика</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_initials']}\n"
                                                    f"<b>Рост</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['height']}\n"
                                                    f"<b>Вес</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['weight']}\n"
                                                    f"<b>Верхнее и нижнее давление</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['upper_and_lower_pressure']}\n"
                                                    f"<b>Адрес электронной почты</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['email']}\n"
                                                    f"<b>Номер телефона</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['phone_number']}\n"
                                                    f"<b>Профессия</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['workplace']}\n"
                                                    f"<b>Место работы</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['position']}\n"
                                                    f"<b>Должность</b>: {incurance_live_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['profession']}\n",
                                                    reply_markup=paymant_keyboard)

            mas = pdf.download_document(message.chat.id, "preliminary_calculation")
            mas+=pdf.download_document(message.chat.id, "policy")
            if mas != None:
                for i in mas:
                    if i[-4:] in [".jpg",".png",".jpeg",".bmp"]:
                        for j in [".jpg",".png",".jpeg",".bmp"]:
                            if i[-4:]==j:
                                try:
                                    bot.send_photo(admin_id,open(i, 'rb'))
                                except Exception as e:
                                    pass
                    else:
                        try:
                            bot.send_document(admin_id, open(i, 'rb'))
                        except Exception as e:
                            pass
            incurance_live_storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                            state="waiting_confirm_live")
            pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="preliminary_calculation")
            pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="policy")
        bot.register_next_step_handler(message, confirm_paymant)

    @bot.callback_query_handler(
        func=lambda call: call.data.split("[]")[0] == "paymant" and str(call.message.chat.id) == admin_id)
    def confirm_paymant(call: CallbackQuery):

        bot.send_message(admin_id,
                         text='Отправьте ссылку для оплаты')
        tg_id = call.data.split("[]")[1]
        print(tg_id)

        def send_documents(message: Message):
            bot.send_message(chat_id=tg_id,
                             text="Ссылка для оплаты полиса"
                                  f"{message.text}")

        bot.register_next_step_handler(message, send_documents)