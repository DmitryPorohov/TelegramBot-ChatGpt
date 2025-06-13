from aiogram.types import FSInputFile
import os

from .enum_path import ResourcePath, Extensions


class Resource:
	"""
	Класс для работы с ресурсами, такими как изображения и текстовые файлы.

	:param file_name: Имя файла, используемое для генерации путей к ресурсам.
	"""
	
	def __init__(self, file_name: str):
		self._file_name = file_name
	
	@property
	def photo(self):
		"""
		Получает объект изображения, если он существует.

		:return: Объект изображения или None, если файл не найден.
		"""
		photo_path = os.path.join(ResourcePath.IMAGES.value, self._file_name + Extensions.JPG.value)
		if os.path.exists(photo_path):
			return FSInputFile(photo_path)
		return None
	
	@property
	def text(self):
		"""
		Получает текст из файла, если он существует.

		:return: Содержимое текстового файла или None, если файл не найден.
		"""
		text_path = os.path.join(ResourcePath.MESSAGES.value, self._file_name + Extensions.TXT.value)
		if os.path.exists(text_path):
			with open(text_path, 'r', encoding='UTF-8') as file:
				return file.read()
		return None
	
	def as_kwargs(self) -> dict[str, FSInputFile | str]:
		"""
		Возвращает словарь с ресурсами в виде ключей и значений.

		:return: Словарь с изображением и текстом.
		"""
		return {'photo': self.photo, 'caption': self.text}
