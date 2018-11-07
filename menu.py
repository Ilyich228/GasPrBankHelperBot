import telebot.types

authorized = False


def draw_menu(bot, chat_id, message_id):
    keyboard = telebot.types.InlineKeyboardMarkup()

    if not authorized:
        auth_btn = telebot.types.InlineKeyboardButton(text='Войти в аккаунт.', callback_data='auth')
        keyboard.add(auth_btn)

    poll_btn = telebot.types.InlineKeyboardButton(text='Опрос.', callback_data='poll')

    auth_req = '(Требуется войти в аккаунт)'
    card_text = 'Оформить карту.'

    if not authorized:
        card_text += auth_req

    card_btn = telebot.types.InlineKeyboardButton(text=card_text, callback_data='card')

    pay_text = 'Платежи и переводы.'

    if not authorized:
        pay_text += auth_req

    pay_btn = telebot.types.InlineKeyboardButton(text=pay_text, callback_data='pay')
    info_btn = telebot.types.InlineKeyboardButton(text='Информация о банке.', callback_data='info')
    faq_btn = telebot.types.InlineKeyboardButton(text='Часто задаваемые вопросы.', callback_data='faq')

    keyboard.row(poll_btn)
    keyboard.row(card_btn)
    keyboard.row(pay_btn)
    keyboard.row(info_btn)
    keyboard.row(faq_btn)

    bot.edit_message_text('ля', chat_id, message_id, reply_markup=keyboard)
