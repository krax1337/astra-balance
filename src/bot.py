import config
import telebot
import balance
import utils
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    regiter_user(message)

    output = "/add чтобы добавить карту\n/status чтобы вывести баланс карт\n/help или /status чтобы вывести это сообщение"

    bot.reply_to(message, output)


def regiter_user(message):
    try:
        utils.create_user_db(message.chat.id)
    except:
        pass


@bot.message_handler(commands=['echo'])
def send_echo(message):

    this_message = str(message.text).split("/echo")[1].split(' ')[2]

    bot.send_message(message.chat.id, "Ты написал мне {}".format(this_message))


@bot.message_handler(commands=['add'])
def add_card(message):

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Отмена ❌')
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id, 'Ввведите номер карты и имя (через пробел)', reply_markup=markup)
    bot.register_next_step_handler(msg, check_card_number)


@bot.message_handler(commands=['status'])
def print_status(message):

    chat_id = message.chat.id

    cards = utils.update_balance(chat_id)

    output = ''

    for card in cards:
        output += "Номер карты: " + str(card['card_number']) + "\n" + str(
            card['card_name']) + " - " + str(card['balance']) + " тенге\n\n"

    bot.send_message(
        chat_id, output)


def check_card_number(message):
    if "Отмена" in message.text:
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        return

    chat_id = message.chat.id
    text = message.text

    if text.split(' ', 1)[0].isdigit() and len(text.split(' ', 1)[0]) == 10 and len(text) > 10:
        try:
            balance.getBalance(text.split(' ', 1)[0])
        except:
            msg = bot.send_message(
                message.chat.id, "Проверьте правильность введеного номера")
            bot.register_next_step_handler(msg, check_card_number)
            return

        try:
            text = text.split(' ', 1)
            utils.add_card_db(chat_id, int(text[0]), text[1])
        except:
            msg = bot.send_message(chat_id, 'Такая карта уже существуеет.')
            bot.register_next_step_handler(msg, check_card_number)
            return

        markup = types.ReplyKeyboardRemove()
        msg = bot.send_message(
            chat_id, 'Спасибо, карта сохранена.', reply_markup=markup)
    else:
        msg = bot.send_message(
            chat_id, 'Номер карты состоит из 10 цифр, название может быть любым.\nНапример: 123456789 Карта Нурбека')
        bot.register_next_step_handler(msg, check_card_number)
        return


@bot.message_handler(content_types=["text"])
def send_balance(message):

    bot.send_message(
        message.chat.id, "Введи /help или /start, чтобы вывести список команд")


if __name__ == '__main__':
    bot.infinity_polling()
