import telebot
import poll
from states import *

with open('token.txt') as f:
    bot = telebot.TeleBot(f.read())


@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    ok_btn = telebot.types.InlineKeyboardButton(text='Да.', callback_data='1')
    no_btn = telebot.types.InlineKeyboardButton(text='Нет.', callback_data='2')
    keyboard.row(ok_btn, no_btn)
    bot.send_message(message.chat.id, 'Вы являетесь клиентом гаспромбанка?', reply_markup=keyboard)

    set_state(message.chat.id, States.S_IS_REGISTERED)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_IS_REGISTERED)
def callback_handler(call):
    if call.data == '1':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Я бы предложил войти в аккаунт если бы знал как.')

        if poll.has_questions():
            keyboard = telebot.types.InlineKeyboardMarkup()
            ok_btn = telebot.types.InlineKeyboardButton(text='Да.', callback_data='1')
            no_btn = telebot.types.InlineKeyboardButton(text='Нет.', callback_data='2')
            keyboard.row(ok_btn, no_btn)

            bot.send_message(text='Вы хотите принять участие в опросе?', chat_id=call.message.chat.id,
                             reply_markup=keyboard)

            set_state(call.message.chat.id, States.S_START_POLL)
        else:
            set_state(call.message.chat.id, States.S_IDLE)
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        ok_btn = telebot.types.InlineKeyboardButton(text='Да.', callback_data='1')
        no_btn = telebot.types.InlineKeyboardButton(text='Нет.', callback_data='2')
        keyboard.row(ok_btn, no_btn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы хотите зарегистрироватся?", reply_markup=keyboard)

        set_state(call.message.chat.id, States.S_REGISTER)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_REGISTER)
def callback_handler(call):
    if call.data == '1':
        bot.edit_message_text('Я хз как.', call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text('Некоторые функции будут недоступны.', call.message.chat.id, call.message.message_id)

    if poll.has_questions():
        keyboard = telebot.types.InlineKeyboardMarkup()
        ok_btn = telebot.types.InlineKeyboardButton(text='Да.', callback_data='1')
        no_btn = telebot.types.InlineKeyboardButton(text='Нет.', callback_data='2')
        keyboard.row(ok_btn, no_btn)

        bot.send_message(text='Вы хотите принять участие в опросе?', chat_id=call.message.chat.id,
                         reply_markup=keyboard)

        set_state(call.message.chat.id, States.S_START_POLL)
    else:
        set_state(call.message.chat.id, States.S_IDLE)


@bot.callback_query_handler(func=lambda call: get_state(call.message.chat.id) == States.S_START_POLL)
def callback_handler(call):
    if call.data == '1':
        poll.show_question(bot, call.message.chat.id)
        set_state(call.message.chat.id, States.S_POLL)
    else:
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
    print('end')
