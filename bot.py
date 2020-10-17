import telebot
import covid
from datetime import datetime
from translate import Translator
import pytz
import os
from boto.s3.connection import S3Connection


token = S3Connection(os.environ['token'])
bot = telebot.TeleBot(token)
covid = covid.Covid(source = 'worldometers')
translator = Translator(from_lang = 'ru' ,to_lang = 'en')


@bot.message_handler(commands=['start'])
def start(message):
	markup = telebot.types.ReplyKeyboardMarkup()
	itembtnhelp = telebot.types.KeyboardButton('/help')
	markup.row(itembtnhelp)

	bot_mess = f'<b>Привет {message.from_user.first_name}!</b> \nя тестовый бот, которые может показать ситуацию по коронавирусу в мире или просто в странах, чтобы узнать подробности нажмите или введите <b>/help</b>'
	bot.send_message(message.from_user.id, bot_mess, reply_markup = markup, parse_mode = 'html')

@bot.message_handler(commands=['help'])
def help(message):
	markup = telebot.types.ReplyKeyboardMarkup()
	item_btn_world = telebot.types.KeyboardButton('Мир')
	item_btn_russia = telebot.types.KeyboardButton('Россия')
	item_btn_usa = telebot.types.KeyboardButton('США')
	item_btn_china = telebot.types.KeyboardButton('Китай')
	item_btn_ukrain = telebot.types.KeyboardButton('Украина')
	
	markup.row(item_btn_russia, item_btn_usa)
	markup.row(item_btn_china, item_btn_ukrain)
	markup.row(item_btn_world)

	bot_mess = '''
	<b>Как пользоваться ботом: </b>
	<b>*Название страны*</b> - выведет статистику по стране
	<b>*Любое слово, не считая названия стран и команды*</b> - выведет статистику по миру
	'''
	bot.send_message(message.from_user.id, bot_mess, reply_markup = markup, parse_mode = 'html')

@bot.message_handler(content_types = ['text'])
def covid19(message):
	translating = translator.translate(text = message.text.lower())
	if translating == 'Afganistan':
		translating = 'Afghanistan'
	get_mess_bot = translating
	final_mess = '''Статистика по коронавирусу в <i>{}</i>:
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
