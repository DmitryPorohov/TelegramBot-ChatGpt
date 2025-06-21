from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.buttons import Button, Buttons, MEDIA_CATEGORIES, MEDIA_GENRES
from classes.callback_data import CelebrityData, QuizData, TranslatorData, MediaData


def ikb_celebrity():
	"""Создает клавиатуру для взаимодействия с выбранной знаменитостью.

	:return: Настроенная клавиатура с кнопками для общения со знаменитостью.
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


def ikb_quiz_select_topic():
	"""
	Создает клавиатуру для выбора темы викторины.

	:return: Настроенная клавиатура с кнопками выбора тем.
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


def ikb_quiz_next(current_topic: QuizData):
	"""
	Создает клавиатуру для перехода к следующему вопросу викторины.

	:param current_topic: Данные о текущей теме викторины.
	:return: Настроенная клавиатура с действиями для викторины.
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
	Creates an inline keyboard for translation options
	:return: InlineKeyboardMarkup with translation options
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


def ikb_media_categories():
	"""
	Создаёт клавиатуру для выбора категории рекомендаций (фильмы, книги, музыка).
	:return: InlineKeyboardMarkup
	"""
	keyboard = InlineKeyboardBuilder()
	for button in MEDIA_CATEGORIES:
		keyboard.button(
			text=str(button.name) if button.name is not None else '',
			callback_data=MediaData(button='select_category', category=str(button.callback) if button.callback is not None else '').pack()
		)
	keyboard.adjust(1)
	return keyboard.as_markup()


def ikb_media_genres(category: str):
	"""
	Создаёт клавиатуру для выбора жанра в выбранной категории.
	:param category: выбранная категория (movies, books, music)
	:return: InlineKeyboardMarkup
	"""
	keyboard = InlineKeyboardBuilder()
	for button in MEDIA_GENRES.get(category, []):
		keyboard.button(
			text=str(button.name) if button.name is not None else '',
			callback_data=MediaData(button='select_genre', category=category, genre=str(button.callback) if button.callback is not None else '').pack()
		)
	keyboard.adjust(2)
	return keyboard.as_markup()


def ikb_media_actions(category: str, genre: str):
	"""
	Создаёт клавиатуру для действий над рекомендацией ("Не нравится", "Закончить").
	:return: InlineKeyboardMarkup
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
