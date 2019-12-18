import config
import telebot
import balance

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	
    bot.reply_to(message, "Введи номер своей карты, чтобы узнать текущий баланс")

@bot.message_handler(content_types=["text"])
def send_balance(message):
    
    if len(str(message.text)) < 10 or not str(message.text).isdigit():
        bot.send_message(message.chat.id, "Введи номер своей карты, чтобы узнать текущий баланс")
    else:
        try:
            balance_of_card = balance.getBalance(message.text)
            bot.send_message(message.chat.id, "Ваш баланс равен {} тенге".format(balance_of_card))
        except:
            bot.send_message(message.chat.id, "Проверьте правильность введеного номера")
            
        


if __name__ == '__main__':
    bot.infinity_polling()