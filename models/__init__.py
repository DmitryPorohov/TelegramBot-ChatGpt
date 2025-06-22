"""
Пакет моделей для Telegram бота.

Содержит все основные классы и структуры данных приложения:
- ChatGpt: Основной класс для работы с ChatGPT API
- GPTMessage: Класс для управления сообщениями GPT
- GPTRole: Класс для работы с ролью GPT
- gpt_client: Глобальный экземпляр клиента ChatGPT
- Button, Buttons: Классы для работы с кнопками
- MEDIA_CATEGORIES, MEDIA_GENRES: Коллекции кнопок
- CelebrityData, QuizData, TranslatorData, MediaData: Callback-данные
- QuizStateData, MediaStateData, CelebrityStateData, GPTStateData: Типы состояний FSM

Пример использования:
    from models import ChatGpt, gpt_client, Button, MEDIA_CATEGORIES
    from models import CelebrityData, QuizData, GPTStateData
"""

from .chat_gpt import ChatGpt, GPTMessage, GPTRole
from .buttons import Button, Buttons, MEDIA_CATEGORIES, MEDIA_GENRES
from .callback_data import (
	CelebrityData, QuizData, TranslatorData, MediaData,
	QuizStateData, MediaStateData, CelebrityStateData, GPTStateData
)

gpt_client = ChatGpt()

__all__ = [
	'ChatGpt', 'GPTMessage', 'GPTRole', 'gpt_client',
	'Button', 'Buttons', 'MEDIA_CATEGORIES', 'MEDIA_GENRES',
	'CelebrityData', 'QuizData', 'TranslatorData', 'MediaData',
	'QuizStateData', 'MediaStateData', 'CelebrityStateData', 'GPTStateData'
]
