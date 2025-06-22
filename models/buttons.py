"""
Модуль для работы с кнопками интерфейса.

Содержит классы для создания и управления кнопками в Telegram боте:
- Button: Класс для отдельной кнопки с именем и callback
- Buttons: Коллекция кнопок с итерацией
- MEDIA_CATEGORIES: Предопределенные кнопки категорий медиа
- MEDIA_GENRES: Предопределенные кнопки жанров для каждой категории

Основные возможности:
- Создание кнопок с именами и callback-данными
- Загрузка имен кнопок из файлов промптов
- Автоматическая загрузка кнопок знаменитостей
- Создание кнопок для категорий и жанров медиа

Зависимости:
- pathlib: Работа с путями файлов
- os: Работа с файловой системой
- common: Основные компоненты приложения
"""

import os
from pathlib import Path
from typing import Union, Optional, List

from common import ResourcePath, Extensions, MediaCategory, MediaGenre, MEDIA_CATEGORY_NAMES, MEDIA_GENRE_NAMES, MEDIA_GENRES_BY_CATEGORY


class Button:
	"""
	Класс для представления кнопки в интерфейсе.
	
	Предоставляет функциональность для создания кнопок с именами
	и callback-данными, включая загрузку имен из файлов.
	
	Attributes:
		name (Optional[str]): Отображаемое имя кнопки
		callback (Optional[str]): Callback-данные кнопки
		_path (Optional[Path]): Путь к файлу с именем кнопки
	"""
	
	def __init__(self, *args: Union[str, None]) -> None:
		"""
		Инициализирует кнопку с заданным путем и опциональным колбэком.
		
		Args:
			*args: Имя кнопки и колбэк, либо имя файла для получения 
				   имени кнопки из файла.
				
		Raises:
			ValueError: Если передано больше двух аргументов
		"""
		self.name: Optional[str] = None
		self.callback: Optional[str] = None
		self._path: Optional[Path] = None
		path = None
		
		if len(args) == 1:
			path = args[0]
			self.callback = path
		elif len(args) == 2:
			self.name, self.callback = args
		elif len(args) > 2:
			raise ValueError("Button() принимает один или два аргумента")
		if self.name is None and path is not None:
			self._path = Path(ResourcePath.PROMPTS.value, f'{path}{Extensions.TXT.value}')
			self.name = self.load_name()
	
	def load_name(self) -> Optional[str]:
		"""
		Загружает имя знаменитости из текстового файла.
		
		Returns:
			str | None: Имя знаменитости, если файл найден и прочитан
		"""
		if self._path is None:
			return None
		with open(self._path, 'r', encoding='UTF-8') as txt_file:
			return self._extract_celebrity_name(txt_file.readline())
	
	@staticmethod
	def _extract_celebrity_name(input_string: str) -> Optional[str]:
		"""
		Извлекает имя знаменитости из строки промпта.
		
		Извлекает текст из строки, начиная с 6-го знака и заканчивая 
		перед запятой (формат: "Ты - ИМЯ, описание...").
		
		Args:
			input_string: Исходная строка промпта
			
		Returns:
			str | None: Извлеченное имя или None, если строка пустая
		"""
		if not input_string:
			return None
		
		start_index = 5  # Начинаем с 6 знака (индекс 5)
		comma_index = input_string.find(',')
		
		if comma_index == -1:
			# Если запятая не найдена, возвращаем подстроку от start_index до конца
			return input_string[start_index:].strip()
		
		return input_string[start_index:comma_index].strip()


class Buttons:
	"""
	Коллекция кнопок с поддержкой итерации.
	
	Предоставляет функциональность для работы с множеством кнопок,
	включая автоматическую загрузку кнопок из файлов.
	
	Attributes:
		buttons (List[Button]): Список кнопок в коллекции
	"""
	
	def __init__(self, buttons: Optional[List[Button]] = None) -> None:
		"""
		Инициализирует коллекцию кнопок.
		
		Args:
			buttons: Список кнопок или None для автоматической загрузки
		"""
		self.buttons: List[Button] = self._read_buttons() if buttons is None else buttons
	
	def __iter__(self):
		"""
		Возвращает итератор для кнопок.
		
		Returns:
			Iterator[Button]: Итератор по кнопкам
		"""
		return iter(self.buttons)
	
	def __next__(self):
		"""
		Возвращает следующую кнопку и удаляет её из списка.
		
		Returns:
			Button: Следующая кнопка
			
		Raises:
			StopIteration: Если кнопки закончились
		"""
		while self.buttons:
			return self.buttons.pop(0)
		raise StopIteration

	@staticmethod
	def _read_buttons() -> List[Button]:
		"""
		Загружает кнопки из файлов, начинающихся с 'talk_'.
		
		Сканирует папку с промптами и создает кнопки для всех файлов,
		начинающихся с префикса 'talk_'.
		
		Returns:
			List[Button]: Список загруженных кнопок
		"""
		resource_path = os.listdir(ResourcePath.PROMPTS.value)
		# Получаем список файлов, которые начинаются с 'talk_'
		buttons_list = [file for file in resource_path if file.startswith('talk_')]
		buttons = [Button(file.split('.')[0]) for file in buttons_list]
		return buttons


def create_media_category_buttons() -> List[Button]:
	"""
	Создает кнопки для категорий медиа.
	
	Returns:
		List[Button]: Список кнопок категорий медиа
	"""
	return [
		Button(MEDIA_CATEGORY_NAMES[category], category.value)
		for category in MediaCategory
	]


def create_media_genre_buttons(category: MediaCategory) -> List[Button]:
	"""
	Создает кнопки жанров для указанной категории медиа.
	
	Args:
		category: Категория медиа
		
	Returns:
		List[Button]: Список кнопок жанров
	"""
	genres = MEDIA_GENRES_BY_CATEGORY.get(category, [])
	return [
		Button(MEDIA_GENRE_NAMES[genre], genre.value)
		for genre in genres
	]


# Кнопки для категорий рекомендаций (для обратной совместимости)
MEDIA_CATEGORIES = create_media_category_buttons()

# Кнопки жанров для каждой категории (для обратной совместимости)
MEDIA_GENRES = {
	category.value: create_media_genre_buttons(category)
	for category in MediaCategory
}
