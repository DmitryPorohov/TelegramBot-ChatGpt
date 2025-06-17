from dataclasses import dataclass
from aiogram.filters.callback_data import CallbackData


@dataclass
class CelebrityData(CallbackData, prefix="celebrity"):
	button: str
	file_name: str


@dataclass
class QuizData(CallbackData, prefix="quiz"):
	button: str
	topic: str
	topic_name: str


class TranslatorData(CallbackData, prefix="translator"):
	button: str
	direction: str

