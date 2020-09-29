import telebot
import covid

token = open('token.txt', 'r').readline()
bot = telebot.TeleBot(token)
covid = covid.Covid(source = 'worldometers')

@bot.message_handler(commands=['start'])
def start(message):
	bot_mess = f'<b>Привет {message.from_user.first_name}!</b> \nя тестовый бот, которые может показать ситуацию по каронавирусу в мире или просто в странах, чтобы узнать подробности введите команду <b>/help</b>'
	bot.send_message(message.from_user.id, bot_mess, parse_mode = 'html')

bot.polling(none_stop = True)
