from enum import Enum

states = {}


class States(Enum):
    S_IDLE = 0

    S_IS_REGISTERED = 1
    S_REGISTER = 2

    S_POLL = 3

    S_INFO = 4


def get_state(user_id):     # TODO database
    if user_id in states:
        return states[user_id]
    else:
        return States.S_IDLE


def set_state(user_id, state):      # TODO database
    states[user_id] = state

