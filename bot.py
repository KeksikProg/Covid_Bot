import telebot
import covid
from datetime import datetime
from translate import Translator
import pytz

token = open('token.txt', 'r').readline()
bot = telebot.TeleBot(token)
covid = covid.Covid(source = 'worldometers')
translator = Translator(from_lang = 'ru' ,to_lang = 'en')


@bot.message_handler(commands=['start'])
def start(message):
	bot_mess = f'<b>Привет {message.from_user.first_name}!</b> \nя тестовый бот, которые может показать ситуацию по каронавирусу в мире или просто в странах, чтобы узнать подробности введите команду <b>/help</b>'
	bot.send_message(message.from_user.id, bot_mess, parse_mode = 'html')

@bot.message_handler(commands=['help'])
def help(message):
	bot_mess = '''
	<b>Основные команды бота:</b>
	<b>/start</b> - Стартовое сообщение
	<b>/help</b> - выводит список всех команд
	<b>*Название страны*</b> - выведет статистику по стране
	<b>*Любое слово, не считая названия стран и команды*</b> - выведет статистику по миру
	'''
	bot.send_message(message.from_user.id, bot_mess, parse_mode = 'html')

@bot.message_handler(content_types = ['text'])
def covid19(message):
	translating = translator.translate(text = message.text)
	get_mess_bot = translating
	final_mess = '''Статистика по каронавирусу в <i>{}</i>:
					<b>Зараженные:</b> <i>{:,}</i>
					<b>Выздоровевшие:</b> <i>{:,}</i>
					<b>Смерти:</b> <i>{:,}</i>
					<b>Время:</b> <i>{}</i>'''

	try:
		country = covid.get_status_by_country_name(translating)
		bot.send_message(
			message.from_user.id,
			final_mess.format(
				message.text,
				country['confirmed'],
				country['recovered'],
				country['deaths'],
				datetime.now(pytz.timezone('Europe/Moscow'))),
			parse_mode = 'html')
	except ValueError:
		bot.send_message(
			message.from_user.id, 
			final_mess.format('Мире', 
								covid.get_total_confirmed_cases(), 
								covid.get_total_recovered(),
								covid.get_total_deaths(),
								datetime.now(pytz.timezone('Europe/Moscow'))),
			parse_mode = 'html')




bot.polling(none_stop = True)
