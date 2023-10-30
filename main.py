import telebot.types
import telebot_router
import telebot

from app import bot
import app.handlers
from app.handlers.commands import *

from telebot.types  import BotCommand
start_command = BotCommand("/start", "Запуск бота")


if __name__ == '__main__':
    bot.set_my_commands([
        start_command
    ])
    bot.set_chat_menu_button()

    bot.polling(none_stop=True)

