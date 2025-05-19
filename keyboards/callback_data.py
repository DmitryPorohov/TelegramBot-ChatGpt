
from aiogram.filters.callback_data import CallbackData

class CelebrityData(CallbackData, prefix='CD'):
	button: str
	file_name: str