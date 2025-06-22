"""
Модуль с определениями callback данных и типов состояний для Telegram бота.

Содержит классы для структурирования данных callback-запросов
от inline кнопок и типизированные словари для состояний FSM.

Callback данные:
- CelebrityData: Данные для выбора знаменитости
- QuizData: Данные для викторины
- TranslatorData: Данные для переводчика
- MediaData: Данные для рекомендаций медиа

Типы состояний:
- QuizStateData: Состояние викторины
- MediaStateData: Состояние рекомендаций медиа
- CelebrityStateData: Состояние разговора со знаменитостью
- GPTStateData: Состояние разговора с GPT

Основные возможности:
- Структурированные callback-данные для inline кнопок
- Типизированные словари для состояний FSM
- Интеграция с aiogram для обработки callback-запросов

Зависимости:
- aiogram: Фреймворк для Telegram ботов
- typing: Типизация данных
- .chat_gpt: GPTMessage для состояний
"""

from aiogram.filters.callback_data import CallbackData
from typing import TypedDict, Dict
from aiogram.types import FSInputFile
from .chat_gpt import GPTMessage


class CelebrityData(CallbackData, prefix="celebrity"):
	"""
	Callback данные для выбора знаменитости.
	
	Содержит информацию о выбранной знаменитости для начала диалога.
	
	Attributes:
		button (str): Идентификатор кнопки
		file_name (str): Имя файла промпта знаменитости
	"""
	button: str
	file_name: str


class QuizData(CallbackData, prefix="quiz"):
	"""
	Callback данные для викторины.
	
	Содержит информацию о выбранной теме викторины и действиях пользователя.
	
	Attributes:
		button (str): Действие пользователя
		topic (str): Идентификатор темы
		topic_name (str): Название темы
	"""
	button: str
	topic: str
	topic_name: str


class TranslatorData(CallbackData, prefix="translator"):
	"""
	Callback данные для переводчика.
	
	Содержит информацию о направлении перевода.
	
	Attributes:
		button (str): Действие пользователя
		direction (str): Направление перевода
	"""
	button: str
	direction: str


class MediaData(CallbackData, prefix="media"):
	"""
	Callback данные для рекомендаций медиа.
	
	Содержит информацию о выбранной категории, жанре и действиях пользователя.
	
	Attributes:
		button (str): Действие пользователя (select_category, select_genre, dislike, finish)
		category (str): Выбранная категория медиа
		genre (str): Выбранный жанр
	"""
	button: str  # действие: select_category, select_genre, dislike, finish
	category: str = ""
	genre: str = ""


# Типы состояний FSM
class QuizStateData(TypedDict):
	"""
	Типизированный словарь для данных состояния викторины.
	
	Содержит:
	- messages: GPTMessage для диалога с ChatGPT
	- photo: Фотография для отображения
	- score: Текущий счет пользователя
	- callback: Данные callback для навигации
	"""
	messages: GPTMessage
	photo: FSInputFile
	score: int
	callback: QuizData


class MediaStateData(TypedDict):
	"""
	Типизированный словарь для данных состояния рекомендаций медиа.
	
	Содержит:
	- category: Выбранная категория медиа
	- genre: Выбранный жанр
	- last_rec: Последняя рекомендация
	- disliked: Список нежелательного контента
	- messages: GPTMessage для диалога с ChatGPT
	- photo: Фотография для отображения
	"""
	category: str
	genre: str
	last_rec: Dict[str, str]
	disliked: list[str]
	messages: GPTMessage
	photo: FSInputFile


class CelebrityStateData(TypedDict):
	"""
	Типизированный словарь для данных состояния разговора со знаменитостью.
	
	Содержит:
	- messages: GPTMessage для диалога с ChatGPT
	- photo: Фотография знаменитости
	"""
	messages: GPTMessage
	photo: FSInputFile


class GPTStateData(TypedDict):
	"""
	Типизированный словарь для данных состояния разговора с ChatGPT.
	
	Содержит:
	- messages: GPTMessage для диалога с ChatGPT
	- photo: Фотография для отображения
	"""
	messages: GPTMessage
	photo: FSInputFile

