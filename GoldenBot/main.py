import telebot
from telebot import types

# Токен вашего бота
TOKEN = '6592904765:AAEg2zgzujZnosLqkB1-u9f9Y2xoDRbyb5U'

# Создание бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных о пользователях
users = {}


# Инициализация клавиатуры с кнопками главного меню
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_profile = types.KeyboardButton('Профиль')
    btn_invite = types.KeyboardButton('Заработать')
    btn_stats = types.KeyboardButton('Статистика')
    btn_withdraw = types.KeyboardButton('Вывести USDT')
    btn_support = types.KeyboardButton('Тех. Поддержка')
    markup.row(btn_profile, btn_invite)
    markup.row(btn_stats, btn_withdraw)
    markup.row(btn_support)
    return markup


# Обработчик команды /start для начала работы с ботом
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    referral_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    if user_id not in users:
        users[user_id] = {'invited': 0, 'balance_usdt': 0, 'referral_id': referral_id, 'invited_by': None}

    if referral_id and referral_id != str(user_id):
        if referral_id in users:
            users[referral_id]['invited'] += 1
            users[user_id]['invited_by'] = referral_id
            users[referral_id]['balance_usdt'] += 0.05  # Начисляем бонус за приглашение
            bot.send_message(referral_id, f"Пользователь с ID {user_id} перешёл по вашей ссылке!")

    bot.send_message(user_id, "Добро пожаловать в Золотой Бот!", reply_markup=create_main_menu())


# Обработчик кнопки "Тех. Поддержка"
@bot.message_handler(func=lambda message: message.text == 'Тех. Поддержка')
def tech_support(message):
    user_id = message.from_user.id
    bot.send_message(user_id,
                     "🔘 Опишите свою проблему подробно (приложив скрины, более понятное описание) и мы вам ответим в ближайшее время!")


# Обработчик кнопки "Выдать USDT"
@bot.message_handler(func=lambda message: message.text == 'Выдать USDT')
def reward_user(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите сумму USDT для начисления на ваш баланс: ")


@bot.message_handler(func=lambda message: message.text == 'Посмотреть сколько приглашений')
def referalls(message):
    user_id = message.from_user.id
    user_data = users.get(user_id, {})
    invited = user_data.get('invited', 0)
    bot.send_message(user_id, f"Количество приглашенных пользователей: {invited}")


# Обработчик кнопки "Вывести USDT"
@bot.message_handler(func=lambda message: message.text == 'Вывести USDT')
def withdraw_usdt(message):
    user_id = message.from_user.id
    user_data = users.get(user_id, {})
    balance_usdt = user_data.get('balance_usdt', 0)

    if balance_usdt < 1:
        bot.send_message(user_id, f"У вас на счету {balance_usdt} USDT. Минимальная сумма вывода - 1 USDT.",
                         reply_markup=create_main_menu())
        return

    # Логика вывода USDT и отправка уведомления
    admin_message = f"Пользователь {user_id} запросил вывод {balance_usdt} USDT."
    bot.send_message(user_id, "Ваш запрос на вывод принят. Ожидайте обработки.", reply_markup=create_main_menu())


# Обработчик кнопки "Удалить аккаунт"
@bot.message_handler(func=lambda message: message.text == 'Удалить аккаунт')
def delete_account(message):
    user_id = message.from_user.id
    if user_id in users:
        del users[user_id]
        bot.send_message(user_id, "Ваш аккаунт удален из системы.")
    else:
        bot.send_message(user_id, "Ваш аккаунт не найден в системе.")


# Обработчик кнопки "Профиль"
@bot.message_handler(func=lambda message: message.text == 'Профиль')
def profile(message):
    user_id = message.from_user.id
    user_data = users.get(user_id, {})
    invited = user_data.get('invited', 0)
    balance_usdt = user_data.get('balance_usdt', 0)
    profile_info = (
        f"Профиль пользователя:\n"
        f"ID: {user_id}\n"
        f"Приглашено людей: {invited}\n"
        f"Баланс: {balance_usdt} USDT"
    )
    bot.send_message(user_id, profile_info, reply_markup=create_main_menu())

    # Обработчик кнопки "Заработать"
    @bot.message_handler(func=lambda message: message.text == 'Заработать')
    def invite(message):
        user_id = message.from_user.id
        user_data = users.get(user_id, {})
        invited = user_data.get('invited', 0)
        referral_link = f"https://t.me/Zolotoibot?start={user_id}"
        invite_text = (
            f"💎 Зарабатывать USDT можно приглашая друзей в нашего бота по своей специальной ссылке\n\n"
            f"🛞 Реф.ссылка: {referral_link}\n\n"
            f"👤 Мои рефералы: {invited}\n\n"
            f"⭐️ Награда за реферала 0.05 USDT"
        )
        bot.send_message(user_id, invite_text, reply_markup=create_main_menu())

    # Обработчик кнопки "Статистика"
    @bot.message_handler(func=lambda message: message.text == 'Статистика')
    def bot_stats(message):
        user_id = message.from_user.id
        total_users = len(users)
        total_invited = sum(user['invited'] for user in users.values())
        total_balance = sum(user['balance_usdt'] for user in users.values())
        stats_info = (
            f"Статистика бота:\n"
            f"Общее количество пользователей: {total_users}\n"
            f"Общее количество приглашений: {total_invited}\n"
            f"Общий баланс пользователей: {total_balance} USDT"
        )
        bot.send_message(user_id, stats_info, reply_markup=create_main_menu())

    # Обработчик всех текстовых сообщений, чтобы пользователь мог отправить вопрос в тех. поддержку
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_id = message.from_user.id
        if message.text == 'Тех. Поддержка':
            bot.send_message(user_id,
                             "🔘 Опишите свою проблему подробно (приложив скрины, более понятное описание) и мы вам ответим в ближайшее время!")
        else:
            bot.send_message(user_id, "Извините, я не понимаю ваш запрос. Вы можете воспользоваться кнопками меню.",
                             reply_markup=create_main_menu())

    # Основной блок запуска бота
    if name == "main":
        bot.polling()