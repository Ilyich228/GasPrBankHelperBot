import telebot
import poll
import menu
from utils import YES_NO_KEYBOARD_MARKUP, OK_KEYBOARD_MARKUP, RETURN_KEYBOARD_MARKUP
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
                              call.message.chat.id, call.message.message_id, reply_markup=OK_KEYBOARD_MARKUP)

        set_state(call.message.chat.id, States.S_INFO)
    else:
        bot.edit_message_text('Вы хотите зарегистрироватся?', call.message.chat.id, call.message.message_id,
                              reply_markup=YES_NO_KEYBOARD_MARKUP)

        set_state(call.message.chat.id, States.S_REGISTER)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_REGISTER)
def callback_handler(call):
    if call.data == 'yes':
        bot.edit_message_text('Я хз как.', call.message.chat.id, call.message.message_id,
                              reply_markup=OK_KEYBOARD_MARKUP)
    else:
        bot.edit_message_text('Некоторые функции будут недоступны.', call.message.chat.id, call.message.message_id,
                              reply_markup=OK_KEYBOARD_MARKUP)

    set_state(call.message.chat.id, States.S_INFO)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_POLL)
def callback_handler(call):
    poll.check_answer(call.data)

    if poll.has_questions():
        poll.show_question(bot, call.message.chat.id)
    else:
        bot.message_handler('Спасибо за прохождение опроса.', call.message.chat.id, call.message.message_id,
                            reply_markup=OK_KEYBOARD_MARKUP)

        set_state(call.message.chat.id, States.S_INFO)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_IDLE)
def callback_handler(call):
    if call.data == 'auth':
        bot.edit_message_text('Вы являетесь клиентом гаспромбанка?', call.message.chat.id, call.message.message_id,
                              reply_markup=YES_NO_KEYBOARD_MARKUP)

        set_state(call.message.chat.id, States.S_IS_REGISTERED)
    elif call.data == 'poll':
        if poll.has_questions():
            poll.show_question(bot, call.message.chat.id)
            set_state(call.message.chat.id, States.S_POLL)
        else:
            pass    # TODO

    elif call.data == 'card':
        pass    # TODO
    elif call.data == 'pay':
        pass    # TODO
    elif call.data == 'info':
        bot.edit_message_text(('«Газпромбанк» (Акционерное общество) – '
                               'один из крупнейших универсальных финансовых'
                               'институтов России, предоставляющий широкий'
                               'спектр банковских, финансовых, инвестиционных'
                               'продуктов и услуг корпоративным и частным'
                               'клиентам, финансовым институтам,'
                               'институциональным и частным инвесторам.'),
                              call.message.chat.id, call.message.message_id, reply_markup=RETURN_KEYBOARD_MARKUP)

        set_state(call.message.chat.id, States.S_INFO)
    elif call.data == 'faq':
        pass    # TODO


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_INFO)
def callback_handler(call):
    if call.data == 'back' or call.data == 'ok':
        menu.draw_menu(bot, call.message.chat.id, call.message.message_id)
        set_state(call.message.chat.id, States.S_IDLE)


if __name__ == '__main__':
    print('start')

    bot.polling()
