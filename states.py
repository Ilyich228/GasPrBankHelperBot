from abc import ABC, abstractmethod
import telebot.types
import survey

states = {}


class State(ABC):
    def __init__(self, bot, chat_id, data={}):
        self.bot = bot
        self.chat_id = chat_id
        self.data = data

        self.on_state_loaded()

    def change_state(self, state):
        states[self.chat_id] = state

    def on_state_loaded(self):
        pass

    @abstractmethod
    def on_message(self, message):
        pass


class StartState(State):
    def on_state_loaded(self):
        if survey.questions_queue:
            keyboard = telebot.types.InlineKeyboardMarkup()
            ok_btn = telebot.types.InlineKeyboardButton(text='Пройти опрос.')
            no_btn = telebot.types.InlineKeyboardButton(text='Позже.')
            keyboard.add(ok_btn)
            keyboard.add(no_btn)
            self.bot.send_message(self.chat_id, 'Хотите поучавствовать в опросе?', reply_markup=keyboard)
        else:
            pass  # skip survey

    def on_message(self, message):
        if message.text == 'Пройти опрос.':
            self.change_state(survey.SurveyState())
        else:
            pass    # skip survey
