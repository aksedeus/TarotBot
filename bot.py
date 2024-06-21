# bot.py
import random
from datetime import datetime
import telebot
from telebot import types
from telebot.types import LabeledPrice

from config import API_TOKEN, provider_token
from auth import register_user, login_user, show_main_menu
from db import add_payment, get_payment_count, get_bot_uses_remaining, decrease_bot_uses
from tarot import TAROT_CARDS
from horoscope import horoscope_parts, zodiacs
from compatibility import relationship_factors
from numerology import specifications


bot = telebot.TeleBot(API_TOKEN)

api_key = provider_token

prices = [LabeledPrice(label='Test Product', amount=8000)]  # 1000 = 10.00 RUB

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Бот Мистик в Телеграме предлагает вам возможность изучить магию карт Таро, Гороскопов, Совместимости и Нумерологии. ✨\n\n"
                          " Вы сможете получить толкования различных раскладов для разных жизненных ситуаций и узнать, как применить мистическую мудрость Таро в повседневной жизни. 🔮\n\n"
                          " Откройте для себя мир искусства предсказаний и духовной глубины с помощью бота Таро в Телеграме! 💜")
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, зарегистрируйтесь или войдите командой /register или /login.")

@bot.message_handler(commands=['register'])
def register(message):
    register_user(bot, message)

@bot.message_handler(commands=['login'])
def login(message):
    login_user(bot, message)

@bot.message_handler(commands=['tarot'])
def ask_how_many_cards(message):
    user_id = message.from_user.id
    uses_remaining = get_bot_uses_remaining(user_id)

    if uses_remaining > 0:
        decrease_bot_uses(user_id)
        askMarkup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('Карта дня', callback_data='1')
        button2 = types.InlineKeyboardButton('Три карты', callback_data='3')
        button3 = types.InlineKeyboardButton('Пять карт', callback_data='5')
        button4 = types.InlineKeyboardButton('Девять карт', callback_data='9')
        askMarkup.add(button1, button2, button3, button4)

        bot.send_message(message.chat.id, "Сколько карт вы хотите выбрать? 🃏\nКаждая карта - это ответ, на заданный вами вопрос по теме 🌟\n", reply_markup=askMarkup)
    else:
        bot.send_message(message.chat.id,
                         "У вас закончились использования. Хотите пополнить? Используйте /pay, чтобы приобрести 25 использований.")
@bot.callback_query_handler(func=lambda call: call.data in ['1', '3', '5', '9'])
def handle_card_selection(call):
    global num_cards
    num_cards = int(call.data)

    askMarkup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Любовь ❤️', callback_data='Любовь')
    button2 = types.InlineKeyboardButton('Работа 🛠️', callback_data='Работа')
    button3 = types.InlineKeyboardButton('Здоровье 💪', callback_data='Здоровье')
    button4 = types.InlineKeyboardButton('На месяц 🌠', callback_data='На месяц')
    askMarkup.add(button1, button2, button3, button4)

    bot.send_message(call.message.chat.id, "На что вы хотите сделать расклад? 🔥\n", reply_markup=askMarkup)

@bot.callback_query_handler(func=lambda call: call.data in ['Любовь', 'Работа', 'Здоровье', 'На месяц'])
def send_tarot_layout(call):

    topic = call.data.upper()

    layout = choose_tarot_cards(num_cards)
    response = f"Расклад на тему '{topic}':\n\n"
    bot.send_message(call.message.chat.id, response)
    for card in layout:
        type = random.randint(1,2)
        value = card['image']
        if type == 1:
            with open(value, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo)
                bot.send_message(call.message.chat.id, f"Карта: {card['name']}\n\nТолкование: {card['meaning']}\n")
        elif type == 2:
            with open(value, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo)
                bot.send_message(call.message.chat.id, f"ПЕРЕВЕРНУТАЯ Карта: {card['name']}\n\nТолкование: {card['reversed']}\n")


    show_main_menu(bot, call.message)
def choose_tarot_cards(num_cards):
    return random.sample(TAROT_CARDS, num_cards)

@bot.message_handler(commands=['horoscope'])
def ask_horoscope(message):
    user_id = message.from_user.id
    uses_remaining = get_bot_uses_remaining(user_id)

    if uses_remaining > 0:
        decrease_bot_uses(user_id)
        askMarkup = types.InlineKeyboardMarkup(row_width=3)
        button1 = types.InlineKeyboardButton('♈ Овен', callback_data='Овен')
        button2 = types.InlineKeyboardButton('♉ Телец', callback_data='Телец')
        button3 = types.InlineKeyboardButton('♊ Близнецы', callback_data='Близнецы')
        button4 = types.InlineKeyboardButton('♋ Рак', callback_data='Рак')
        button5 = types.InlineKeyboardButton('♌ Лев', callback_data='Лев')
        button6 = types.InlineKeyboardButton('♍ Дева', callback_data='Дева')
        button7 = types.InlineKeyboardButton('♎ Весы', callback_data='Весы')
        button8 = types.InlineKeyboardButton('♏ Скорпион', callback_data='Скорпион')
        button9 = types.InlineKeyboardButton('⛎ Змееносец', callback_data='Змееносец')
        button10 = types.InlineKeyboardButton('♐ Стрелец	', callback_data='Стрелец')
        button11 = types.InlineKeyboardButton('♑ Козерог', callback_data='Козерог')
        button12 = types.InlineKeyboardButton('♒ Водолей', callback_data='Водолей')
        button13 = types.InlineKeyboardButton('♓ Рыбы', callback_data='Рыбы')
        askMarkup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12, button13)

        bot.send_message(message.chat.id,
                         "Какой у вас знак зодиака? 🌟",
                         reply_markup=askMarkup)
    else:
        bot.send_message(message.chat.id,
                         "У вас закончились использования. Хотите пополнить? Используйте /pay, чтобы приобрести 25 использований.")


@bot.callback_query_handler(func=lambda call: call.data in ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Змееносец', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы'])
def send_horoscope(call):
    zodiac = zodiacs[call.data]
    topic = call.data.upper()
    response = f"Расклад для знака '{topic}':\n\n"
    response += generate_horoscope(horoscope_parts)

    with open(zodiac, "rb") as photo:
        bot.send_photo(call.message.chat.id, photo, response)

    show_main_menu(bot, call.message)

# Функция для генерации гороскопа
def generate_horoscope(horoscope_parts):
    начало = random.choice(horoscope_parts["Начало"])
    середина = random.choice(horoscope_parts["Середина"])
    конец = random.choice(horoscope_parts["Конец"])
    return f"{начало} {середина} {конец}"

@bot.message_handler(commands=['numerology'])
def ask_gender(message):
    user_id = message.from_user.id
    uses_remaining = get_bot_uses_remaining(user_id)

    if uses_remaining > 0:
        decrease_bot_uses(user_id)
        askMarkup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('Женщина 🙋‍♀️', callback_data='woman')
        button2 = types.InlineKeyboardButton('Мужчина 🙋🏻‍♂️', callback_data='man')
        askMarkup.add(button1, button2)

        bot.send_message(message.chat.id, "Ваш пол? 🌟", reply_markup=askMarkup)
    else:
        bot.send_message(message.chat.id,
                         "У вас закончились использования. Хотите пополнить? Используйте /pay, чтобы приобрести 25 использований.\nЛибо зайдите через день и вам начислятся новые попытки бесплатно!")

@bot.callback_query_handler(func=lambda call: call.data in ['woman', 'man'])
def handle_message(call):
    bot.send_message(call.message.chat.id, "Пожалуйста, введите дату рождения в правильном формате ДД.ММ.ГГГГ")
    bot.register_next_step_handler(call.message, get_birth_date)
def get_birth_date(message):
    try:
        birth_date = message.text.strip()
        matrix_result = analyze_birth_date(birth_date)
        bot.send_message(message.chat.id, matrix_result)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}\nПожалуйста, введите дату рождения в правильном формате ДД.ММ.ГГГГ")

# Функция для анализа даты рождения через алгоритм Матрицы Пифагора
def analyze_birth_date(birth_date):
    # Преобразование даты в список цифр
    day, month, year = map(int, birth_date.split('.'))
    digits = list(map(int, list(f"{day:02}{month:02}{year}")))

    # Вычисление рабочих чисел
    sum_all_digits = sum(digits)
    sum_of_digits = sum(map(int, str(sum_all_digits)))
    third_number = sum_all_digits - 2 * int(str(day)[0])
    fourth_number = sum(map(int, str(third_number)))

    # Все цифры для матрицы
    all_digits = digits + list(map(int, str(sum_all_digits))) + list(map(int, str(sum_of_digits))) + list(map(int, str(third_number))) + list(map(int, str(fourth_number)))

    # Создание матрицы Пифагора
    matrix = {i: 0 for i in range(1, 10)}
    for digit in all_digits:
        if digit != 0:
            matrix[digit] += 1

    # Формирование строки результата
    matrix_result = f"Матрица Пифагора для даты рождения {birth_date}:\n\n"

    # Добавляем интерпретацию каждой позиции в матрице
    interpretation = {
        1: "Единицы 💎 (Характер): ",
        2: "Двойки ⚡️ (Энергия): ",
        3: "Тройки 🔥 (Интерес): ",
        4: "Четверки 💪 (Здоровье): ",
        5: "Пятерки 💡 (Логика): ",
        6: "Шестерки 🛠️ (Труд): ",
        7: "Семерки 🍀 (Удача): ",
        8: "Восьмерки 🛡️ (Долг): ",
        9: "Девятки ❤️ (Память): "
    }

    for i in range(1, 10):
        count = matrix[i]
        if count == 0:
            matrix_result += f"{interpretation[i]}💫\n"
        else:
            matrix_result += f"{interpretation[i]}{'⭐' * count}\n"

    # Рассчитываем дополнительные показатели
    self_esteem = matrix[1] + matrix[2] + matrix[3]
    household = matrix[4] + matrix[5] + matrix[6]
    talent = matrix[7] + matrix[8] + matrix[9]
    goal = matrix[1] + matrix[4] + matrix[7]
    family = matrix[2] + matrix[5] + matrix[8]
    habits = matrix[3] + matrix[6] + matrix[9]
    spirit = matrix[1] + matrix[5] + matrix[9]
    temperament = matrix[3] + matrix[5] + matrix[7]

    # Словарь интерпретаций
    additional_interpretation = {
        "Самооценка": self_esteem,
        "Быт": household,
        "Талант": talent,
        "Цель": goal,
        "Семья": family,
        "Привычки": habits,
        "Дух": spirit,
        "Темперамент": temperament
    }

    # Добавляем интерпретацию дополнительных показателей
    matrix_result += "\nДополнительные показатели 🔮:\n"
    for key, value in additional_interpretation.items():
        if key in specifications and value in specifications[key]:
            description = specifications[key][value]
            matrix_result += f"{key}: {value} - {description}\n"
        else:
            matrix_result += f"{key}: {value}\n"

    return matrix_result

@bot.message_handler(commands=['compatibility'])
def ask_compatibility(message):
    user_id = message.from_user.id
    uses_remaining = get_bot_uses_remaining(user_id)

    if uses_remaining > 0:
        decrease_bot_uses(user_id)
        bot.send_message(message.chat.id, "Пожалуйста, введите дату рождения Партнера 1 в формате ДД.ММ.ГГГГ 🙋‍♀️")
        bot.register_next_step_handler(message, get_first_birth_date)
    else:
        bot.send_message(message.chat.id,
                         "У вас закончились использования. Хотите пополнить? Используйте /pay, чтобы приобрести 25 использований.")
def get_first_birth_date(message):
    try:
        birth_date1 = message.text.strip()
        datetime.strptime(birth_date1, "%d.%m.%Y")
        bot.send_message(message.chat.id, "Теперь введите дату рождения Партнера 2 в формате ДД.ММ.ГГГГ 🙋🏻‍♂️")
        bot.register_next_step_handler(message, get_second_birth_date, birth_date1)
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный формат даты. Пожалуйста, введите дату рождения Партнера 1 в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(message, get_first_birth_date)

def get_second_birth_date(message, birth_date1):
    try:
        birth_date2 = message.text.strip()
        datetime.strptime(birth_date2, "%d.%m.%Y")
        compatibility_result = analyze_compatibility(birth_date1, birth_date2)
        bot.send_message(message.chat.id, compatibility_result)
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный формат даты. Пожалуйста, введите дату рождения Партнера 2 в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(message, get_second_birth_date, birth_date1)

def analyze_compatibility(birth_date1, birth_date2):
    # Преобразование даты в список цифр для обоих партнеров
    day1, month1, year1 = map(int, birth_date1.split('.'))
    digits1 = list(map(int, list(f"{day1:02}{month1:02}{year1}")))

    day2, month2, year2 = map(int, birth_date2.split('.'))
    digits2 = list(map(int, list(f"{day2:02}{month2:02}{year2}")))

    # Функция для расчета матрицы Пифагора
    def calculate_matrix(digits):
        sum_all_digits = sum(digits)
        sum_of_digits = sum(map(int, str(sum_all_digits)))
        third_number = sum_all_digits - 2 * int(str(day1)[0])
        fourth_number = sum(map(int, str(third_number)))
        all_digits = digits + list(map(int, str(sum_all_digits))) + list(map(int, str(sum_of_digits))) + list(map(int, str(third_number))) + list(map(int, str(fourth_number)))
        matrix = {i: 0 for i in range(1, 10)}
        for digit in all_digits:
            if digit != 0:
                matrix[digit] += 1
        return matrix

    # Расчет матриц для обоих партнеров
    matrix1 = calculate_matrix(digits1)
    matrix2 = calculate_matrix(digits2)

    # Анализ совместимости на основе матриц
    compatibility_result = f"Совместимость пары 👩‍❤️‍👨:\n\n"

    # Добавляем интерпретацию характеристик
    compatibility_result += f"Для чего встретились 🎯: {get_description(relationship_factors, 'для чего встретились', matrix1[1] + matrix2[1])}\n\n"
    compatibility_result += f"Как проявляется пара 🔥: {get_description(relationship_factors, 'как проявляется пара', matrix1[2] + matrix2[2])}\n\n"
    compatibility_result += f"Для успешных отношений важно ⭐: {get_description(relationship_factors, 'для успешных отношений важно', matrix1[3] + matrix2[3])}\n\n"
    compatibility_result += f"Проблемы и трудности 🛑: {get_description(relationship_factors, 'проблемы и трудности', matrix1[4] + matrix2[4])}\n\n"
    compatibility_result += f"Задачи пары 🏅: {get_description(relationship_factors, 'задачи пары', matrix1[5] + matrix2[5])}\n\n"
    compatibility_result += f"Причины расставания 🚩: {get_description(relationship_factors, 'причины расставания', matrix1[6] + matrix2[6])}\n"

    return compatibility_result

def get_description(dictionary, key, sum_value):
    return dictionary[key].get(sum_value, "Описание не найдено")

@bot.message_handler(commands=['pay'])
def buy(message):
    bot.send_invoice(
        message.chat.id,
        title="Использования услуг",
        description="Дополнительные 25 использований функций бота",
        provider_token=provider_token,
        currency='RUB',
        prices=prices,
        start_parameter='test-invoice',
        invoice_payload='test-invoice-payload'
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    user_id = message.from_user.id
    amount = message.successful_payment.total_amount
    currency = message.successful_payment.currency
    add_payment(user_id, amount, currency)
    bot.send_message(message.chat.id, "Спасибо за покупку! Ваш платеж обработан.")

@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    username = message.from_user.username
    usage_count = get_bot_uses_remaining(user_id)
    payment_count = get_payment_count(user_id)
    bot.send_message(message.chat.id, f"Ваш профиль 🧙‍♂️:\n\nНикнейм 🔮: {username}\nКоличество покупок 🛒: {payment_count}\nКоличество использований на счету ✅:{usage_count}\nЗайдите через день и вам начислятся новые попытки бесплатно!")

if __name__ == '__main__':
    bot.polling()
