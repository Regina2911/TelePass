from telebot import TeleBot
from config import API_TOKEN, DATABASE
from logic import DatabaseManager

bot = TeleBot(API_TOKEN)

manager = DatabaseManager(DATABASE)
manager.create_tables()

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Hello! I am a simple password manager bot.\n"
        "/add - add password\n"
        "/show - show saved passwords"
    )


@bot.message_handler(commands=['add'])
def add_password(message):
    bot.send_message(message.chat.id, "Enter service name:")
    bot.register_next_step_handler(message, get_service)


def get_service(message):
    user_data[message.chat.id] = {"service": message.text}

    bot.send_message(message.chat.id, "Enter username:")
    bot.register_next_step_handler(message, get_username)


def get_username(message):
    user_data[message.chat.id]["username"] = message.text

    bot.send_message(message.chat.id, "Enter password:")
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    service = user_data[message.chat.id]["service"]
    username = user_data[message.chat.id]["username"]
    password = message.text

    manager.add_password(service, username, password)

    bot.send_message(message.chat.id, "Password saved!")


@bot.message_handler(commands=['show'])
def show_passwords(message):
    data = manager.get_passwords()

    if not data:
        bot.send_message(message.chat.id, "No passwords saved.")
        return

    text = ""

    for service, username, password in data:
        text += f"Service: {service}\nUsername: {username}\nPassword: {password}\n\n"

    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)