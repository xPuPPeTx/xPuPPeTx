import telebot
import threading
import time
import os

from datetime import datetime

bot = telebot.TeleBot("8435012273:AAGSMsX6c8EhqLrvSwPfUYskdAq6neFQg70")

tg_id = '1868194974'

def GetWhiteList():

	if not os.path.isfile('whitelist.txt'):
		with open('whitelist.txt', 'w', encoding='utf-8') as whitelistFile:
			whitelistFile.write('')

	with open('whitelist.txt', 'r', encoding='utf-8') as whitelistFile:
		whitelist = whitelistFile.readlines()

	for w in whitelist:
		whitelist[whitelist.index(w)] = w.split('\n')[0]

	print(whitelist)
	return whitelist

def send_report(id, products):

	filename = f"Отчёт_{str(datetime.now().date())}.txt"

	with open(filename, 'a', encoding='utf-8') as report_file:
		for product in products:
			report_file.write(f'Товар: {product[0]} | Принято: {product[1]}шт. | ПТВ: {product[2]}шт.\n')

	bot.send_document(tg_id, open(filename, 'rb'), caption=f"От @id{id}")

@bot.message_handler(content_types=['text'])
def GetTextMessages(message):

	text = message.text.strip()

	if '/verify' in text:
		bot.send_message(message.from_user.id, str(message.from_user.id))

	elif str(message.from_user.id) in GetWhiteList():
		products = []

		for line in text.split('\n'):
			products.append(line.strip().split('; '))

		send_report(message.from_user.id, products)

bot.polling(none_stop=True, interval=0)
