"""
Модуль обычных клавиатур для Telegram бота.

Содержит функции для создания обычных (Reply) клавиатур,
которые отображаются внизу экрана в Telegram.

Основные функции:
- kb_replay: Создание главного меню с кнопками
- kb_end_talk: Клавиатура для завершения разговора со знаменитостью
- kb_end_gpt: Клавиатура для завершения разговора с ChatGPT

Основные возможности:
- Создание адаптивных клавиатур
- Настройка placeholder текста
- Поддержка one-time клавиатур
- Автоматическое изменение размера

Зависимости:
- aiogram: Фреймворк для Telegram ботов
"""

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_replay(buttons: list[str]):
	"""
	Создает главное меню с кнопками.
	
	Создает обычную клавиатуру с переданными кнопками для навигации
	по основным функциям бота.
	
	Args:
		buttons (list[str]): Список текстов кнопок для меню
		
	Returns:
		ReplyKeyboardMarkup: Настроенная клавиатура с кнопками
	"""
	keyboard = ReplyKeyboardBuilder()
	for button in buttons:
		keyboard.button(
			text=button,
		)
	return keyboard.as_markup(
		resize_keyboard=True,
		input_field_placeholder='Выберете пункт меню...',
	)


def kb_end_talk():
	"""
	Создает клавиатуру для завершения разговора со знаменитостью.
	
	Создает клавиатуру с одной кнопкой "Попрощаться!" для
	завершения диалога со знаменитостью.
	
	Returns:
		ReplyKeyboardMarkup: Настроенная клавиатура с кнопкой завершения
	"""
	keyboard = ReplyKeyboardBuilder()
	keyboard.button(
		text='Попрощаться!',
	)
	return keyboard.as_markup(
		resize_keyboard=True,
		input_field_placeholder='Задайте свой вопрос...',
		one_time_keyboard=True,
	)


def kb_end_gpt():
	"""
	Создает клавиатуру для завершения разговора с ChatGPT.
	
	Создает клавиатуру с одной кнопкой "Закончить" для
	завершения диалога с ChatGPT.
	
	Returns:
		ReplyKeyboardMarkup: Настроенная клавиатура с кнопкой завершения
	"""
	keyboard = ReplyKeyboardBuilder()
	keyboard.button(
		text='Закончить',
	)
	return keyboard.as_markup(
		resize_keyboard=True,
		input_field_placeholder='Задайте свой вопрос...',
		one_time_keyboard=True,
	)