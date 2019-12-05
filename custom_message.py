# -*- coding: utf-8 -*-

from download_bot import Download_Bot

bot = Download_Bot(client_status=True)
controller = True
while controller:
	message = str(input("Insert your message: "))
	if message != 'e':
		bot.whatsapp_send_message(message, bot.to_number, bot.from_number, mode='display')
	else:
		break