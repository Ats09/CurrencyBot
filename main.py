import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n- Показать список доступных валют через команду /values \
    \n- Вывести конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
'- Напомнить, что я могу через команду /help'\

    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key.title(), ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.replace(',', '.').split(' ')

        if len(values) != 3:

            raise APIException('Некорректное количество параметров. '
                               'Ожидается 3 параметра.')

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f"Цена {amount} {base.lower().title()} в {quote.lower().title()} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()
