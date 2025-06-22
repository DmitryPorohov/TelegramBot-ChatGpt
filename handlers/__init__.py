"""
Пакет обработчиков для Telegram бота.

Этот пакет содержит все обработчики сообщений, команд и callback-запросов
для Telegram бота. Организует роутеры в единую структуру для удобного
импорта в основном модуле.

Содержит:
- commands_router: Обработчик команд бота
- callback_router: Обработчик inline кнопок
- messages_router: Обработчик текстовых сообщений

Основные возможности:
- Обработка команд пользователя
- Обработка callback-запросов от inline кнопок
- Обработка текстовых сообщений и состояний FSM
- Интеграция с ChatGPT API

Экспортирует:
- routers: Список всех роутеров для подключения к диспетчеру
"""

from commands import commands_router
from .callback_handlers import callback_router
from .message_handler import messages_router

routers = [
	messages_router,
	commands_router,
	callback_router,
]

__all__ = [
	'routers',
]
