from utils import YES_NO_KEYBOARD_MARKUP
from states import *

questions = [{}]


def start_poll(bot, chat_id):
    if has_questions():
        bot.send_message(chat_id, 'Вы хотите принять участие в опросе?',
                         reply_markup=YES_NO_KEYBOARD_MARKUP)

        set_state(chat_id, States.S_START_POLL)
    else:
        set_state(chat_id, States.S_IDLE)


def has_questions():
    return bool(questions)


def show_question(bot, chat_id):
    pass


def check_answer(answer):
    pass
