from telebot import types
from db import add_user, get_user

def register_user(bot, message):
    user = get_user(message.from_user.id)
    if user:
        bot.reply_to(message, "Вы уже зарегистрированы.")
    else:
        add_user(message.from_user.id, message.from_user.username)
        bot.reply_to(message, "Регистрация прошла успешно!")

def login_user(bot, message):
    user = get_user(message.from_user.id)
    if user:
        bot.reply_to(message, f"Что я могу предложить вам, {message.from_user.username}?")
        show_main_menu(bot, message)
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь или войдите командой /register или /login.")

def show_main_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    tarot_button = types.KeyboardButton('/tarot')
    horoscope_button = types.KeyboardButton('/horoscope')
    compatibility_button = types.KeyboardButton('/compatibility')
    numerology_button = types.KeyboardButton('/numerology')
    profile_button = types.KeyboardButton('/profile')
    pay_button = types.KeyboardButton('/pay')
    markup.add(tarot_button, horoscope_button, compatibility_button, numerology_button, profile_button, pay_button)
    bot.send_message(message.chat.id, "Вы в системе. Выберите команду:\n\n/tarot - расклады Таро\n/horoscope - гороскоп на сегодня.\n/compatibility - совместимость с партнером.\n/numerology - нумерологический прогноз.\n/profile - профиль пользователя.\n/pay - покупка новых предсказаний.", reply_markup=markup)
