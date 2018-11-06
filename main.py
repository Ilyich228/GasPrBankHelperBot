import telebot
import poll
from utils import YES_NO_KEYBOARD_MARKUP
from states import *

with open('token.txt') as f:
    bot = telebot.TeleBot(f.read())


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Вы являетесь клиентом гаспромбанка?', reply_markup=YES_NO_KEYBOARD_MARKUP)

    set_state(message.chat.id, States.S_IS_REGISTERED)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_IS_REGISTERED)
def callback_handler(call):
    if call.data == 'yes':
        bot.edit_message_text('Я бы предложил войти в аккаунт если бы знал как.',
                              call.message.chat.id, call.message.message_id)

        poll.start_poll(bot, call.message.chat.id)
    else:
        bot.edit_message_text('Вы хотите зарегистрироватся?', call.message.chat.id, call.message.message_id,
                              reply_markup=YES_NO_KEYBOARD_MARKUP)

        set_state(call.message.chat.id, States.S_REGISTER)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_REGISTER)
def callback_handler(call):
    if call.data == 'yes':
        bot.edit_message_text('Я хз как.', call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text('Некоторые функции будут недоступны.', call.message.chat.id, call.message.message_id)

    poll.start_poll(bot, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_START_POLL)
def callback_handler(call):
    if call.data == 'yes':
        poll.show_question(bot, call.message.chat.id)
        set_state(call.message.chat.id, States.S_POLL)
    else:
        bot.edit_message_text('Вы можете пройти опрос позже набрав команду которую я еще не придумал.',  # /poll ?
                              call.message.chat.id, call.message.message_id)
        set_state(call.message.chat.id, States.S_IDLE)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_POLL)
def callback_handler(call):
    poll.check_answer(call.data)

    if poll.has_questions():
        poll.show_question(bot, call.message.chat.id)
    else:
        set_state(call.message.char.id, States.S_IDLE)


if __name__ == '__main__':
    print('start')
    bot.polling()
