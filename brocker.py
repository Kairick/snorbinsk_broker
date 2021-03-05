import telebot
from decouple import config

bot = telebot.TeleBot(config('BOT_API'))


def send_message(user_id, stock_name, stock_price):
    message = f'Пора продавать акцию {stock_name}. Цена акции - {stock_price}'
    bot.send_message(user_id, message)
