import telebot
from decouple import config

bot = telebot.TeleBot(config('BOT_API'))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    send_message('hi, man!')


def send_message(message):
    bot.send_message(98344348, message)

bot.polling()