import telebot
from states import states, StartState

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    states[message.chat_id] = StartState(bot, message.chat_id)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    states[message.chat_id].on_message(message)


if __name__ == '__main__':
    bot.polling()
