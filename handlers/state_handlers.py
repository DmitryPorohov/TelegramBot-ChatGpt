"""
Определения состояний для конечного автомата Telegram бота.

Этот модуль содержит все классы состояний, используемые в FSM (Finite State Machine)
для управления диалогами с пользователями в различных режимах работы бота.

Классы состояний:
- ChatGPTRequests: Состояния для разговора с ChatGPT
- CelebrityTalk: Состояния для разговора со знаменитостями
- Quiz: Состояния для викторины
- Translator: Состояния для переводчика
- MediaRecommendation: Состояния для рекомендаций медиа
"""

from aiogram.fsm.state import State, StatesGroup


class ChatGPTRequests(StatesGroup):
	"""
	Состояния для разговора с ChatGPT.
	
	Содержит состояния для управления диалогом с ChatGPT,
	включая ожидание запроса от пользователя.
	"""
	wait_for_request = State()


class CelebrityTalk(StatesGroup):
	"""
	Состояния для разговора со знаменитостями.
	
	Содержит состояния для управления диалогом со знаменитостями,
	включая ожидание ответа от пользователя.
	"""
	wait_for_answer = State()


class Quiz(StatesGroup):
	"""
	Состояния для викторины.
	
	Содержит состояния для управления процессом викторины:
	- wait_for_answer: Ожидание ответа на вопрос
	- select_topic: Выбор темы викторины
	- wait_press_button: Ожидание нажатия кнопки
	"""
	wait_for_answer = State()
	select_topic = State()
	wait_press_button = State()


class Translator(StatesGroup):
	"""
	Состояния для переводчика.
	
	Содержит состояния для управления процессом перевода:
	- select_direction: Выбор направления перевода
	- wait_for_text: Ожидание текста для перевода
	"""
	select_direction = State()
	wait_for_text = State()


class MediaRecommendation(StatesGroup):
	"""
	Состояния для рекомендаций медиа.
	
	Содержит состояния для управления процессом рекомендаций:
	- select_category: Выбор категории медиа
	- select_genre: Выбор жанра
	- wait_for_recommendation: Ожидание рекомендации
	"""
	select_category = State()
	select_genre = State()
	wait_for_recommendation = State()
