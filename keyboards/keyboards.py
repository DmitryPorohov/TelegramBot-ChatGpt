from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_replay(buttons):
	"""
	Создает главное меню с кнопками.

	:param buttons: Список текстов кнопок для меню.
	:return: Объект ReplyKeyboardBuilder с настройками клавиатуры.
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
	Создает клавиатуру для завершения разговора.

	:return: Настроенная клавиатура с кнопкой для прощания.
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
	Создает клавиатуру для завершения разговора.

	:return: Настроенная клавиатура с кнопкой для завершения.
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