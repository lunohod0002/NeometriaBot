import telebot

incurance_live_storage = telebot.StateMemoryStorage()
incurance_property_storage = telebot.StateMemoryStorage()
incurance_live_and_property_storage = telebot.StateMemoryStorage()

'''def set_property_loan_agreement(message: Message):
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
        (message.document.file_name)
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
        (message.document.file_name)
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


def set_year_construction(message: Message):
    incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="year_construction", value=message.text)
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
                         text='Адрес электронной почты',reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, set_email)


def set_email(message: Message):
    incurance_property_storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                        key="email", value=message.text)

    bot.send_message(chat_id=message.chat.id,
                     text='Загрузите действующий полис в фомрмате pdf \n(если нет действующего полиса "далее")')
    bot.register_next_step_handler(message, property_load_policy)


def property_load_policy(message: Message):
    if message.content_type != "document":
        bot.send_message(chat_id=message.chat.id,
                         text='Загрузите действующий полис в фомрмате pdf (если нет действующего полиса "далее")')


    else:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        (incurance_property_storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id))
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
        mas += pdf.download_document(message.chat.id, "policy")
        if mas != None:
            for i in mas:
                if i[-4:] in [".jpg", ".png", ".jpeg", ".bmp"]:
                    for j in [".jpg", ".png", ".jpeg", ".bmp"]:
                        if i[-4:] == j:
                            try:

                                bot.send_photo(admin_id, open(i, 'rb'))

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
    func=lambda call: skip_button_info.filter(call.data) and incurance_property_storage.get_state(
        chat_id=call.message.chat.id,
        user_id=call.message.chat.id) == "set_property_incurance_load_policy")
def property_load_policy(call: CallbackQuery):
    paymant_button = InlineKeyboardButton(text='Отправить ссылку для оплаты...',
                                          callback_data=f"paymant[]{call.message.chat.id}")

    paymant_keyboard = InlineKeyboardMarkup()
    paymant_keyboard.row(paymant_button)
    bot.send_message(chat_id=call.message.chat.id, text='Данные отправлены менеджеру!')
    bot.send_message(chat_id=call.message.chat.id, text='Пожалуйста, ожидайте ссылку на оплату')
    bot.send_message(chat_id=admin_id, text="Оформление полиса\n"
                                            "Страхование жизни\n"
                                            f"<b>ID</b>: @{call.message.from_user.username}\n"
                                            f"<b>Банк</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['bank']}\n"
                                            f"<b>Сумма кредита</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['credit_balance']}\n"
                                            f"<b>Дата рождения</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['birthdate']}\n"
                                            f"<b>Пол</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['sex']}\n"
                                            f"<b>Дата начала действия полиса</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['policy_start_date']}\n"
                                            f"<b>Процентная ставка по кредиту</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['interest_rate']}\n"
                                            f"<b>Номер кредитного договора</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_number']}\n"
                                            f"<b>Дата подписания кредитного договора</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_sign_date']}\n"
                                            f"<b>Дата окончания кредитного договора</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_end_date']}\n"
                                            f"<b>ФИО заемщика</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['contract_initials']}\n"
                                            f"<b>Адрес объекта страхования </b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['address_insurance']}\n"
                                            f"<b>Площадь квартиры</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['address_area']}\n"
                                            f"<b>Этаж</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['floor']}\n"
                                            f"<b>Количество этажей в подъезде </b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['floor_number']}\n"
                                            f"<b>Адрес электронной почты</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['email']}\n"
                                            f"<b>Номер телефона</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['phone_number']}\n"
                                            f"<b>Год постройки дома</b>: {incurance_property_storage.get_data(chat_id=call.message.chat.id, user_id=call.message.chat.id)['year_construction']}\n",
                     reply_markup=paymant_keyboard)
    pdf = PDF()
    mas = pdf.download_document(call.message.chat.id, "preliminary_calculation")
    (mas)

    mas += pdf.download_document(call.message.chat.id, "policy")
    if mas != None:
        for i in mas:
            if i[-4:] in [".jpg", ".png", ".jpeg", ".bmp"]:
                for j in [".jpg", ".png", ".jpeg", ".bmp"]:
                    if i[-4:] == j:
                        try:
                            bot.send_photo(admin_id, open(i, 'rb'))
                        except Exception as e:
                            pass
            else:
                try:
                    bot.send_document(admin_id, open(i, 'rb'))
                except Exception as e:
                    pass
    incurance_property_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.from_user.id,
                                         state="waiting_confirm_live")
    pdf.delete_from_ctalog(telegram_id=call.message.chat.id, catalog="preliminary_calculation")
    pdf.delete_from_ctalog(telegram_id=call.message.chat.id, catalog="policy")
    bot.callback_query_handler(property_confirm_paymant)'''