from aiogram.filters.callback_data import CallbackData


class CelebrityData(CallbackData, prefix='CD'):
	button: str
	file_name: str


class QuizData(CallbackData, prefix='QD'):
	button: str
	topic: str
	topic_name: str
