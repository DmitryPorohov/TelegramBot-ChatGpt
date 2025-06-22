"""
Пакет команд для Telegram бота.

Этот пакет содержит все команды бота, которые пользователи
могут вызывать через слэш-команды в Telegram.

Содержит:
- cmd_start: Команда /start - главное меню
- cmd_random: Команда /random - случайные факты
- cmd_gpt: Команда /gpt - разговор с ChatGPT
- cmd_talk: Команда /talk - разговор со знаменитостями
- cmd_quiz: Команда /quiz - запуск викторины
- cmd_translator: Команда /translator - переводчик
- cmd_media: Команда /media - рекомендации медиа
- commands_router: Роутер для всех команд

Экспортирует:
- Все команды для импорта в других модулях
- commands_router для подключения к диспетчеру
"""

from .commands import cmd_start, cmd_random, cmd_gpt, cmd_talk, cmd_quiz, cmd_translator, cmd_media, commands_router

__all__ = [
	'cmd_start',
	'cmd_random',
	'cmd_gpt',
	'cmd_talk',
	'cmd_quiz',
	'cmd_translator',
	'cmd_media',
	'commands_router'
]
