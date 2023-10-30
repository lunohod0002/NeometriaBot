import telebot

incurance_live_storage = telebot.StateMemoryStorage()
incurance_property_storage = telebot.StateMemoryStorage()
incurance_live_and_property_storage = telebot.StateMemoryStorage()


"""@bot.callback_query_handler(func=lambda call: skip_button_info.filter(call.data) and
                                                  incurance_live_storage.get_state(call.message.chat.id,
                                                                                   call.from_user.id) == "incurance_live")
    def skip_incurance_live_policy(call: CallbackQuery):
        bot.send_message(chat_id=call.message.chat.id, text='Данные отправлены менеджеру!')
        bot.send_message(chat_id=call.message.chat.id, text='Соcтавляем коммерческое предложение...')
        bot.send_message(chat_id=admin_id, text="<b>Предварительный рассчёт</b>\n"
                                                "<b>Страхование жизни</b>\n"
                                                f"<b>ID</b>: @{call.from_user.username}\n"
                                                f"<b>Банк</b>: {incurance_live_storage.get_data(chat_id=call.message.chat.id, user_id=call.from_user.id)['bank']}\n"
                                                f"<b>Сумма кредита</b>: {incurance_live_storage.get_data(chat_id=call.message.chat.id, user_id=call.from_user.id)['credit_balance']}\n"
                                                f"<b>Дата рождения</b>: {incurance_live_storage.get_data(chat_id=call.message.chat.id, user_id=call.from_user.id)['birthdate']}\n"
                                                f"<b>Пол</b>: {incurance_live_storage.get_data(chat_id=call.message.chat.id, user_id=call.from_user.id)['sex']}\n")

        incurance_live_storage.set_state(chat_id=call.message.chat.id, user_id=call.message.from_user.id,
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
                         reply_markup=preliminary_calculation_keyboard)"""