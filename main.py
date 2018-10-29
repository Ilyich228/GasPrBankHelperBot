import telebot

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    pass


if __name__ == '__main__':
    bot.polling()