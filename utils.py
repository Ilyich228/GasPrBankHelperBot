import telebot.types


def create_keyboard_markup(*args):
    keyboard = telebot.types.InlineKeyboardMarkup()

    buttons = []

    for i in args:
        btn = telebot.types.InlineKeyboardButton(text=i['text'], callback_data=i['callback_data'])
        buttons.append(btn)

    keyboard.row(*buttons)

    return keyboard


YES_NO_KEYBOARD_MARKUP = create_keyboard_markup({'text': 'Да.', 'callback_data': 'yes'},
                                                {'text': 'Нет.', 'callback_data': 'no'})
