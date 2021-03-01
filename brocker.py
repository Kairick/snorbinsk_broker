import telebot
from decouple import config

from service import add_new_stock

bot = telebot.TeleBot(config('BOT_API'))


@bot.message_handler(commands=['new'])
def new_stock(message):
    params = message.text.split(' ')
    try:
        price = int(params[2])
    except ValueError:
        return bot.reply_to(message, 'Неверно указана цена')
    if len(params) < 3:
        return bot.reply_to(message, 'Неверное количество параметров')
    if len(params) == 3:
        success = add_new_stock(params, message.from_user.id)

        if success is not None:
            return bot.reply_to(message, f'{params[1]} успешной поставлена на мониторинг')
        else:
            return bot.reply_to(message, 'Произошла ошибка при добавлении акции, попробуйте еще раз')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    send_message('hi, man!')

def send_message(message):
    bot.send_message(98344348, message)

bot.polling()