import telebot.types
from app.keyboards.helpers import share_contact_keyboard
from app import bot
from app.API.PDF import PDF
from telebot.types import CallbackQuery, Message
from app.keyboards.sex import choose_sex_keyboard, female_button_info, male_button_info
from app.keyboards.skip import *
from app.config import admin_id
from app.keyboards.confirm import *
from app.keyboards.start.text import insurance_property_button_info
import os
from app.keyboards.preliminary_calculation import preliminary_calculation_pdf_button_info, \
    preliminary_calculation_text_button_info
from app.services import incurance_property_storage,incurance_live_storage


@bot.callback_query_handler(func=lambda call: insurance_property_button_info.filter(call.data))
def incurance_property(call: CallbackQuery):
    incurance_live_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state="incurance_propertyd")

    incurance_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state="incurance_property")
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Укажите наименование банка, выдавшего ипотечный кредит')

    def set_property_incurance_property_bank(message: Message):
        print(message)
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="bank", value=message.text)
        bot.send_message(chat_id=call.message.chat.id, text='Введите сумму кредита (остаток кредитной задолжнности')

        bot.register_next_step_handler(call.message, set_property_incurance_property_credit_balance)

    bot.register_next_step_handler(call.message, set_property_incurance_property_bank)


def set_property_incurance_property_credit_balance(message: Message):
    incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                    key="credit_balance", value=message.text)
    bot.send_message(chat_id=message.chat.id, text='Введите дату рождения заемщика в формате ДД.ММ.ГГГГ')

    bot.register_next_step_handler(message, set_property_incurance_property_birthdate)


def set_property_incurance_property_birthdate(message: Message):
    incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                    key="birthdate", value=message.text)
    bot.send_message(chat_id=message.chat.id, text="Выберите пол заемщика", reply_markup=choose_sex_keyboard)
    incurance_live_storage.set_state(message.chat.id, message.from_user.id,state="incurance_property")



    @bot.callback_query_handler(func=lambda call: male_button_info.filter(call.data) or
                                                  female_button_info.filter(call.data) and
                                                  incurance_property_storage.get_state(call.message.chat.id,
                                                                                   call.from_user.id) == "incurance_property")
    def choose_incurance_property_sex(call: CallbackQuery):
        print(call)
        incurance_property_storage.set_data(chat_id=call.message.chat.id, user_id=call.from_user.id, key="sex",
                                        value=call.data)
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "пропустить"',
                              reply_markup=skip_keyboard)


        def set_property_incurance_property_policy(message: Message):
            if message.content_type != "document":
                bot.send_message(chat_id=message.chat.id,
                                 text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "пропустить"',
                                 reply_markup=skip_keyboard)
                bot.register_next_step_handler(call.message, set_property_incurance_property_policy)

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
                                                        "Страхование имущества\n"
                                                        f"<b>ID</b>: @{call.from_user.username}\n"
                                                        f"<b>Банк</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['bank']}\n"
                                                        f"<b>Сумма кредита</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['credit_balance']}\n"
                                                        f"<b>Дата рождения</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['birthdate']}\n"
                                                        f"<b>Пол</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['sex']}\n")
                mas = pdf.download_document(message.chat.id, "preliminary_calculation")
                if mas != None:
                    for i in mas:
                        bot.send_document(admin_id, open(i, 'rb'))
                        os.remove(i)
                incurance_property_storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
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

        bot.register_next_step_handler(call.message, set_property_incurance_property_policy)




    @bot.callback_query_handler(
        func=lambda call: call.data.split("[]")[0] == "text")
    def get_text_preliminary_calculation(call: CallbackQuery):
        incurance_property_storage.set_state(call.message.chat.id,
                                         call.from_user.id, state="incurance_propertys")
        tg_id = call.data.split("[]")[1]
        incurance_property_storage.set_state(tg_id, tg_id, state="preliminary_calculation_policy")
        bot.send_message(chat_id=admin_id, text='Напишите коммерческое предложение')

        def send_text_preliminary_calculation(message: Message):
            tg_id = call.data.split("[]")[1]
            bot.send_message(chat_id=tg_id,
                             text="Ваше коммерческое предложение:\n"
                                  f"{message.text}", reply_markup=confirm_keyboard)

        bot.register_next_step_handler(call.message, send_text_preliminary_calculation)


    @bot.callback_query_handler(
        func=lambda call: call.data.split("[]")[0] == "pdf")
    def get_pdf_preliminary_calculation(call: CallbackQuery):
        incurance_property_storage.set_state(call.message.chat.id, call.from_user.id,
                                         state="preliminary_calculation_policy")

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
        func=lambda call: call.data == "reject" and incurance_property_storage.get_state(chat_id=call.message.chat.id,
                                                                                     user_id=call.from_user.id) != "incurance_policy")
    def set_property_reject(call: CallbackQuery):
        bot.send_message(chat_id=admin_id, text=f"@{call.from_user.username} отклонил предложение")
        bot.send_message(chat_id=call.message.chat.id, text='Предложение отклонено')
        incurance_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                                         state="incurance_policy")


    @bot.callback_query_handler(
        func=lambda call: preliminary_calculation_confirm_button_info.filter(call.data) and
                          incurance_property_storage.get_state(chat_id=call.message.chat.id,
                                                           user_id=call.from_user.id) != "incurance_policy"
    )
    def set_property_confirm(call: CallbackQuery):
        bot.send_message(chat_id=admin_id,
                         text=f"@{call.from_user.username} подтвердил коммерческое предложение")
        incurance_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                                         state="incurance_policy")

        bot.send_message(call.message.chat.id,
                         text='Отлично! Теперь введите дату начала действия полиса')

        def set_property_policy_start_date(message: Message):
            incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                            key="policy_start_date", value=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text='Введите процентную ставку по кредиту')

            bot.register_next_step_handler(message, set_property_interest_rate)

        bot.register_next_step_handler(call.message, set_property_policy_start_date)


    def set_property_interest_rate(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="interest_rate", value=message.text)
        bot.send_message(chat_id=message.chat.id, text='Введите номер кредитного договора')

        bot.register_next_step_handler(message, set_property_contract_number)


    def set_property_contract_number(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_number", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите дату подписания кредитного договора в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(message, set_property_contract_sign_date)


    def set_property_contract_sign_date(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_sign_date", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите дату окончания кредитного договора в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(message, set_property_contract_end_date)


    def set_property_contract_end_date(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_end_date", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Введите ФИО")
        bot.register_next_step_handler(message, set_property_contract_initials)


    def set_property_contract_initials(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="contract_initials", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Загрузите фото паспорта (первая страница")
        bot.register_next_step_handler(message, set_property_first_pasport)


    def set_property_first_pasport(message: Message):
        if message.content_type != "photo":
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите фото паспорта (первая страница")
            bot.register_next_step_handler(message, set_property_first_pasport)
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

            bot.register_next_step_handler(message, set_property_registration_pasport)


    def set_property_registration_pasport(message: Message):
        if message.content_type != "photo":
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите фото паспорта (адрес регистрации)")

            bot.register_next_step_handler(message, set_property_registration_pasport)
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

            bot.register_next_step_handler(message, set_property_loan_agreement)


    def set_property_loan_agreement(message: Message):
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
                             text="Загрузите выписку ЕГРН")
            bot.register_next_step_handler(message, set_property_EGRN)
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
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите выписку ЕГРН")
            bot.register_next_step_handler(message, set_property_EGRN)
            os.remove(message.document.file_name)

        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Загрузите все страницы кредитного договора.")

            bot.register_next_step_handler(message, set_property_loan_agreement)


    def set_property_EGRN(message: Message):
        if str(message.content_type) == "document":
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print(message.document.file_name)
            with open(message.document.file_name, 'wb') as f:
                f.write(downloaded_file)

            pdf = PDF()
            pdf.upload_document(telegram_id=message.chat.id, file_name=message.document.file_name,
                                    key='ЕГРН',
                                    catalog="policy")
            os.remove(message.document.file_name)
            bot.send_message(chat_id=message.chat.id,
                             text="Отлично! Теперь введите адрес обьекта регистрации")
            bot.register_next_step_handler(message, set_address_insurance)


    def set_address_insurance(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="address_insurance", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Площадь квартиры:")
        bot.register_next_step_handler(message, set_address_area)


    def set_address_area(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="address_area", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Количество этажей в подъезде:")
        bot.register_next_step_handler(message, set_floor_number)


    def set_floor_number(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="floor_number", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Ваш этаж:")
        bot.register_next_step_handler(message, set_floor)


    def set_floor(message: Message):

            incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                            key="floor", value=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text="Пожалуйста введите год постройки дома")
            bot.register_next_step_handler(message, set_year_construction)




    def set_year_construction (message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="year_construction", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Адрес электронный почты:")
        bot.register_next_step_handler(message, set_email)

    def set_email(message: Message):
        incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="email", value=message.text)
        bot.send_message(chat_id=message.chat.id,
                         text="Необходимо поделиться номером телефона", reply_markup=share_contact_keyboard)
        bot.register_next_step_handler(message, set_phone_number)

    def set_phone_number(message: Message):
        if message.content_type != "contact":
            bot.send_message(chat_id=message.chat.id,
                             text="Необходимо поделиться номером телефона", reply_markup=share_contact_keyboard)
            bot.register_next_step_handler(message, set_phone_number)
        else:
            with open("users.txt", "w+") as f:
                f.write(
                    f"{message.chat.id}[]{message.from_user.username}[]@{message.from_user.username}[]{message.contact.phone_number}")
            incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                            key="phone_number", value=message.contact.phone_number)
            bot.send_message(chat_id=message.chat.id,
                             text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "пропустить"',reply_markup=skip_keyboard)
            bot.register_next_step_handler(message, property_load_policy)


    def property_load_policy(message: Message):
        if message.content_type != "document":
            bot.send_message(chat_id=message.chat.id,
                             text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "пропустить"',
                             reply_markup=skip_keyboard)
            bot.register_next_step_handler(message, property_load_policy)

        else:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print(incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id))
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
                                                    "Страхование имущества\n"
                                                    f"<b>ID</b>: @{message.from_user.username}\n"
                                                    f"<b>Банк</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['bank']}\n"
                                                    f"<b>Сумма кредита</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['credit_balance']}\n"
                                                    f"<b>Дата рождения</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['birthdate']}\n"
                                                    f"<b>Пол</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['sex']}\n"
                                                    f"<b>Дата начала действия полиса</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['policy_start_date']}\n"
                                                    f"<b>Процентная ставка по кредиту</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['interest_rate']}\n"
                                                    f"<b>Номер кредитного договора</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_number']}\n"
                                                    f"<b>Дата подписания кредитного договора</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_sign_date']}\n"
                                                    f"<b>Дата окончания кредитного договора</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_end_date']}\n"
                                                    f"<b>ФИО заемщика</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['contract_initials']}\n"
                                                    f"<b>Адрес объекта страхования </b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['address_insurance']}\n"
                                                    f"<b>Площадь квартиры</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['address_area']}\n"
                                                    f"<b>Этаж</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['floor']}\n"
                                                    f"<b>Количество этажей в подъезде </b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['floor_number']}\n"
                                                    f"<b>Адрес электронной почты</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['email']}\n"

                                                    f"<b>Номер телефона</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['phone_number']}\n"
                                                    f"<b>Год постройки дома</b>: {incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['year_construction']}\n",
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
            incurance_property_storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                            state="waiting_confirm_property")
            pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="preliminary_calculation")
            pdf.delete_from_ctalog(telegram_id=message.chat.id, catalog="policy")

        @bot.callback_query_handler(
                func=lambda call: call.data.split("[]")[0] == "paymant"and str(call.message.chat.id)==admin_id)

        def property_confirm_paymant(call: CallbackQuery):

            bot.send_message(admin_id,
                             text='Отправьте ссылку для оплаты')
            tg_id = call.data.split("[]")[1]
            print(tg_id)
            def property_send_documents(message: Message):
                bot.send_message(chat_id=tg_id,
                                 text="Ссылка для оплаты полиса"
                                      f"{message.text}")
            bot.register_next_step_handler(call.message, property_send_documents)



