from enum import Enum

states = {}


class States(Enum):
    S_IDLE = '0'
    S_START = '1'
    S_IS_REGISTERED = '2'
    S_REGISTER = '3'

    S_START_POLL = '4'
    S_POLL = '5'


def get_state(user_id):     # TODO database
    if user_id in states:
        return states[user_id]
    else:
        return States.S_START


def set_state(user_id, state):      # TODO database
    states[user_id] = state
