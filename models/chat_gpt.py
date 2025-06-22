"""
Модуль для работы с ChatGPT API.

Содержит классы для взаимодействия с OpenAI API:
- GPTMessage: Класс для управления сообщениями GPT
- ChatGpt: Синглтон-класс для работы с ChatGPT API

Основные возможности:
- Загрузка промптов из файлов
- Управление диалогом с ChatGPT
- Асинхронные запросы к OpenAI API
- Поддержка прокси и обработка ошибок

Зависимости:
- openai: Клиент для OpenAI API
- httpx: HTTP клиент для прокси
- os: Работа с переменными окружения
- common: Основные компоненты приложения
- config: Конфигурация приложения
- exception: Пользовательские исключения
"""

import os
import openai
import httpx
from typing import Optional, List, Dict
from common import GPTRole, Extensions, ResourcePath
from exception import FileOperationError, ConfigurationError, APIConnectionError
from config import Config


class GPTMessage:
	"""
	Класс для управления сообщениями GPT.
	
	Предоставляет функциональность для загрузки промптов из файлов
	и управления диалогом с ChatGPT.
	
	Attributes:
		prompt_file (str): Имя файла промпта с расширением
		message_list (list): Список сообщений для отправки в API
	"""
	
	def __init__(self, prompt: str):
		"""
		Инициализирует объект GPTMessage.
		
		Args:
			prompt (str): Имя промпта без расширения
		"""
		self.prompt_file = prompt + Extensions.TXT.value
		self.message_list = self._init_message()
	
	def _init_message(self) -> List[Dict[str, str]]:
		"""
		Инициализирует список сообщений с системным промптом.
		
		Returns:
			List[Dict[str, str]]: Список сообщений с системным промптом
		"""
		message = {
			'role': GPTRole.SYSTEM.value,
			'content': self._load_prompt(),
		}
		return [message]
	
	def _load_prompt(self) -> str:
		"""
		Загружает промпт из файла.
		
		Returns:
			str: Содержимое файла промпта
			
		Raises:
			FileOperationError: Если файл не может быть прочитан
		"""
		prompt_path = os.path.join(ResourcePath.PROMPTS.value, self.prompt_file)
		try:
			with open(prompt_path, 'r', encoding='UTF-8') as file:
				prompt = file.read()
			if not prompt.strip():
				raise FileOperationError(f"Prompt file {self.prompt_file} is empty")
			return prompt
		except FileNotFoundError:
			raise FileOperationError(f"Prompt file {self.prompt_file} not found at {prompt_path}")
		except Exception as e:
			raise FileOperationError(f"Error reading prompt file: {str(e)}")
	
	def update(self, role: GPTRole, message: str):
		"""
		Добавляет новое сообщение в диалог.
		
		Args:
			role (GPTRole): Роль отправителя сообщения
			message (str): Содержание сообщения
			
		Raises:
			ValueError: Если сообщение пустое
		"""
		if not message.strip():
			raise ValueError("Message cannot be empty")
		message_dict = {
			'role': role.value,
			'content': message,
		}
		self.message_list.append(message_dict)


class ChatGpt:
	"""
	Синглтон-класс для работы с ChatGPT API.
	
	Предоставляет асинхронные методы для отправки запросов к OpenAI API
	с поддержкой прокси и обработкой ошибок.
	
	Attributes:
		_gpt_token (str): Токен для доступа к OpenAI API
		_proxy (Optional[str]): Прокси-сервер (опционально)
		_model (str): Модель GPT для использования
		_client (AsyncOpenAI): Клиент OpenAI
	"""
	
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		"""Реализует паттерн Singleton."""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance
	
	def __init__(self, model: Optional[str] = None):
		"""
		Инициализирует клиент ChatGPT.
		
		Args:
			model (str, optional): Модель GPT для использования. 
								 Если не указана, используется из конфигурации.
			
		Raises:
			ConfigurationError: Если не установлен GPT_TOKEN
		"""
		self._gpt_token = Config.GPT_TOKEN
		self._proxy = Config.PROXY
		self._model = model or Config.GPT_MODEL
		
		if not self._gpt_token:
			raise ConfigurationError("GPT_TOKEN environment variable is not set")
		
		self._client = self._create_client()
	
	def _create_client(self):
		"""
		Создает экземпляр клиента AsyncOpenAI.
		
		Returns:
			AsyncOpenAI: Экземпляр клиента OpenAI
			
		Raises:
			APIConnectionError: При сбое создания клиента
		"""
		try:
			gpt_client = openai.AsyncClient(
				api_key=self._gpt_token,
				http_client=httpx.AsyncClient(
					timeout=Config.REQUEST_TIMEOUT,
					proxy=self._proxy
				)
			)
			return gpt_client
		except Exception as e:
			raise APIConnectionError(f"Failed to create OpenAI client: {str(e)}")
	
	async def request(self, message: GPTMessage) -> str:
		"""
		Отправляет запрос к ChatGPT API.
		
		Args:
			message (GPTMessage): Объект с сообщениями для отправки
			
		Returns:
			str: Ответ от ChatGPT
			
		Raises:
			APIConnectionError: При сбое запроса к API
		"""
		try:
			response = await self._client.chat.completions.create(
				messages=message.message_list,
				model=self._model,
			)
			if not response.choices:
				raise APIConnectionError("No response received from the API")
			content = response.choices[0].message.content
			if content is None:
				raise APIConnectionError("Empty response content from the API")
			return content
		except openai.APIError as e:
			raise APIConnectionError(f"OpenAI API error: {str(e)}")
		except httpx.RequestError as e:
			raise APIConnectionError(f"Network error: {str(e)}")
		except Exception as e:
			raise APIConnectionError(f"Unexpected error during API request: {str(e)}")
