from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_replay(buttons):
	keyboard = ReplyKeyboardBuilder()
	for button in buttons:
		keyboard.button(
			text=button,
		)
	return keyboard.as_markup(
		resize_keyboard=True,
		input_field_placeholder='Выберете пункт меню...',
	)
