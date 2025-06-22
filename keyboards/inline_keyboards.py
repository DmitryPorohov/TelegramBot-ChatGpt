"""
Модуль для создания инлайн-клавиатур.

Содержит функции для создания различных типов инлайн-клавиатур:
- get_translation_keyboard: Клавиатура для выбора направления перевода
- get_quiz_keyboard: Клавиатура для викторины
- get_media_keyboard: Клавиатура для выбора категорий и жанров медиа
- get_gpt_keyboard: Клавиатура для диалога с GPT

Зависимости:
- aiogram: Фреймворк для Telegram ботов
- core: Основные компоненты приложения
- models: Модели данных
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common import MediaCategory, MediaGenre, MEDIA_CATEGORY_NAMES, MEDIA_GENRE_NAMES, MEDIA_GENRES_BY_CATEGORY
from models import Button, Buttons, MEDIA_CATEGORIES, MEDIA_GENRES, CelebrityData, QuizData, TranslatorData, MediaData


def ikb_celebrity() -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для выбора знаменитости.
	
	Создает inline клавиатуру с кнопками для всех доступных знаменитостей,
	загружая их из файлов промптов.
	
	Returns:
		InlineKeyboardMarkup: Клавиатура с кнопками знаменитостей
	"""
	keyboard = InlineKeyboardBuilder()
	buttons = Buttons()
	for button in buttons:
		keyboard.button(
			text=button.name if button.name is not None else '',
			callback_data=CelebrityData(
				button='select_celebrity',
				file_name=button.callback if button.callback is not None else '',
			),
		)
	keyboard.adjust(1)
	return keyboard.as_markup()


def ikb_quiz_select_topic() -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для выбора темы викторины.
	
	Создает inline клавиатуру с предопределенными темами викторины:
	Python, Математика, Биология.
	
	Returns:
		InlineKeyboardMarkup: Клавиатура с кнопками тем викторины
	"""
	keyboard = InlineKeyboardBuilder()
	buttons_quiz_thems = [
		Button('Язык Python', 'quiz_prog'),
		Button('Математика', 'quiz_math'),
		Button('Биология', 'quiz_biology')
	]
	buttons = Buttons(buttons_quiz_thems)
	for button in buttons:
		keyboard.button(
			text=button.name if button.name is not None else '',
			callback_data=QuizData(
				button='select_topic',
				topic=button.callback if button.callback is not None else '',
				topic_name=button.name if button.name is not None else ''
			)
		)
	keyboard.adjust(1)
	return keyboard.as_markup()


def ikb_quiz_next(current_topic: QuizData) -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для навигации в викторине.
	
	Создает inline клавиатуру с кнопками для продолжения викторины,
	смены темы или завершения.
	
	Args:
		current_topic (QuizData): Данные о текущей теме викторины
		
	Returns:
		InlineKeyboardMarkup: Клавиатура с действиями для викторины
	"""
	keyboard = InlineKeyboardBuilder()
	buttons_quiz_next = [
		Button('Дальше', 'next_question'),
		Button('Сменить тему', 'change_topic'),
		Button('Закончить', 'finish_quiz')
	]
	buttons = Buttons(buttons_quiz_next)
	for button in buttons:
		keyboard.button(
			text=button.name if button.name is not None else '',
			callback_data=QuizData(
				button=button.callback if button.callback is not None else '',
				topic=current_topic.topic if current_topic.topic is not None else '',
				topic_name=current_topic.topic_name if current_topic.topic_name is not None else ''
			)
		)
	keyboard.adjust(2, 1)
	return keyboard.as_markup()


def ikb_translator() -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для выбора направления перевода.
	
	Создает inline клавиатуру с кнопками для выбора направления
	перевода: английский на русский или русский на английский.
	
	Returns:
		InlineKeyboardMarkup: Клавиатура с опциями перевода
	"""
	builder = InlineKeyboardBuilder()
	builder.add(InlineKeyboardButton(
		text="ENG -> RUS",
		callback_data=TranslatorData(button="eng_rus", direction="eng_rus").pack()
	))
	builder.add(InlineKeyboardButton(
		text="RUS -> ENG",
		callback_data=TranslatorData(button="rus_eng", direction="rus_eng").pack()
	))
	builder.adjust(2)
	return builder.as_markup()


def ikb_media_categories() -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для выбора категории медиа.
	
	Создает inline клавиатуру с кнопками для выбора категории
	рекомендаций: фильмы, книги, музыка.
	
	Returns:
		InlineKeyboardMarkup: Клавиатура с категориями медиа
	"""
	keyboard = InlineKeyboardBuilder()
	for button in MEDIA_CATEGORIES:
		keyboard.button(
			text=str(button.name) if button.name is not None else '',
			callback_data=MediaData(button='select_category', category=str(button.callback) if button.callback is not None else '').pack()
		)
	keyboard.adjust(1)
	return keyboard.as_markup()


def ikb_media_genres(category: str) -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для выбора жанра в выбранной категории.
	
	Создает inline клавиатуру с кнопками жанров для выбранной
	категории медиа (фильмы, книги, музыка).
	
	Args:
		category (str): Выбранная категория (movies, books, music)
		
	Returns:
		InlineKeyboardMarkup: Клавиатура с жанрами для категории
	"""
	keyboard = InlineKeyboardBuilder()
	for button in MEDIA_GENRES.get(category, []):
		keyboard.button(
			text=str(button.name) if button.name is not None else '',
			callback_data=MediaData(button='select_genre', category=category, genre=str(button.callback) if button.callback is not None else '').pack()
		)
	keyboard.adjust(2)
	return keyboard.as_markup()


def ikb_media_actions(category: str, genre: str) -> InlineKeyboardMarkup:
	"""
	Создает клавиатуру для действий с рекомендациями.
	
	Создает inline клавиатуру с кнопками для взаимодействия
	с полученной рекомендацией: "Не нравится" и "Закончить".
	
	Args:
		category (str): Выбранная категория медиа
		genre (str): Выбранный жанр
		
	Returns:
		InlineKeyboardMarkup: Клавиатура с действиями для рекомендаций
	"""
	keyboard = InlineKeyboardBuilder()
	keyboard.button(
		text='Не нравится',
		callback_data=MediaData(button='dislike', category=category, genre=genre).pack()
	)
	keyboard.button(
		text='Закончить',
		callback_data=MediaData(button='finish').pack()
	)
	keyboard.adjust(2)
	return keyboard.as_markup()
