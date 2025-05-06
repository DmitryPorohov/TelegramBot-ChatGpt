from datetime import datetime


def on_start():
	time_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
	print(f'Bot is started at {time_now}')


def on_shutdown():
	time_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
	print(f'Bot is down at {time_now}')
