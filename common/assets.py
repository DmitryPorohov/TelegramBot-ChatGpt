"""
Модуль для работы с ресурсами приложения.

Содержит класс Resource для работы с изображениями и текстовыми файлами,
предоставляя удобный интерфейс для доступа к ресурсам приложения.

Основные возможности:
- Загрузка изображений из папки resources/images
- Загрузка текстовых файлов из папки resources/messages
- Получение ресурсов по имени файла без расширения
"""

from aiogram.types import FSInputFile
import os

from .enums import ResourcePath, Extensions


class Resource:
	"""
	Класс для работы с ресурсами приложения.
	
	Предоставляет методы для получения изображений и текстовых файлов
	по имени файла без расширения.
	
	Attributes:
		_file_name (str): Имя файла без расширения
	"""
	
	def __init__(self, file_name: str):
		"""
		Инициализирует объект Resource.
		
		Args:
			file_name (str): Имя файла без расширения
		"""
		self._file_name = file_name
	
	@property
	def photo(self) -> FSInputFile | None:
		"""
		Получает объект изображения.
		
		Returns:
			FSInputFile | None: Объект изображения или None, если файл не найден
		"""
		photo_path = os.path.join(ResourcePath.IMAGES.value, self._file_name + Extensions.JPG.value)
		if os.path.exists(photo_path):
			return FSInputFile(photo_path)
		return None
	
	@property
	def text(self) -> str | None:
		"""
		Получает текст из файла.
		
		Returns:
			str | None: Содержимое текстового файла или None, если файл не найден
		"""
		text_path = os.path.join(ResourcePath.MESSAGES.value, self._file_name + Extensions.TXT.value)
		if os.path.exists(text_path):
			with open(text_path, 'r', encoding='UTF-8') as file:
				return file.read()
		return None
	
	def as_kwargs(self) -> dict[str, FSInputFile | str | None]:
		"""
		Возвращает словарь с ресурсами.
		
		Returns:
			dict[str, FSInputFile | str | None]: Словарь с изображением и текстом
		"""
		return {'photo': self.photo, 'caption': self.text} 