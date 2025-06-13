from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.buttons import Button, Buttons
from classes.callback_data import CelebrityData, QuizData


def ikb_celebrity():
	"""Создает клавиатуру для взаимодействия с выбранной знаменитостью.

	:return: Настроенная клавиатура с кнопками для общения со знаменитостью.
	"""
	keyboard = InlineKeyboardBuilder()
	buttons = Buttons()
	for button in buttons:
		keyboard.button(
			text=button.name,
			callback_data=CelebrityData(
				button='select_celebrity',
				file_name=button.callback,
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
			text=button.name,
			callback_data=QuizData(
				button='select_topic',
				topic=button.callback,
				topic_name=button.name,
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
			text=button.name,
			callback_data=QuizData(
				button=button.callback,
				topic=current_topic.topic,
				topic_name=current_topic.topic_name
			)
		)
	keyboard.adjust(2, 1)
	return keyboard.as_markup()
