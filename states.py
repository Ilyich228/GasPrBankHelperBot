from abc import ABC, abstractmethod

states = {}


class State(ABC):
    def __init__(self, bot, chat_id, data={}):
        self.bot = bot
        self.chat_id = chat_id
        self.data = data

    def change_state(self, state):
        states[self.chat_id] = state

    def on_start(self):
        self.bot.send_message("start string")

    def on_help(self):
        self.bot.send_message("help string")

    @abstractmethod
    def on_message(self, message):
        raise NotImplementedError()


class StartState(State):
    pass
