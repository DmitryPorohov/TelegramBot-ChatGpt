import os
import openai
import httpx
from .enum_path import GPTRole, Extensions

from classes.enum_path import ResourcePath


class GPTError(Exception):
	"""Базовое исключение для ошибок, связанных с GPT"""
	pass


class FileOperationError(GPTError):
	"""Исключение для ошибок файловой операции"""
	pass


class APIConnectionError(GPTError):
	"""Исключение для ошибок подключения к API"""
	pass


class ConfigurationError(GPTError):
	"""Исключение, вызванное ошибками конфигурации"""
	pass


class GPTMessage:
	
	def __init__(self, prompt: str):
		self.prompt_file = prompt + Extensions.TXT.value
		self.message_list = self._init_message()
	
	def _init_message(self) -> list[dict[str, str]]:
		message = {
			'role': GPTRole.SYSTEM.value,
			'content': self._load_prompt(),
		}
		return [message]
	
	def _load_prompt(self) -> str:
		"""
		Открывает и считывает файл приглашения
		:return: str -> содержимое файла приглашения
		:raises: FileOperationError, если файл не может быть прочитан
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
		Добавляет новую роль и сообщение в беседу
		:param role: GPTRole enum значение
		:param message: Содержание сообщения
		:raises: ValueError, если сообщение пустое
		"""
		if not message.strip():
			raise ValueError("Message cannot be empty")
		message = {
			'role': role.value,
			'content': message,
		}
		self.message_list.append(message)


class ChatGpt:
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance
	
	def __init__(self, model: str = 'gpt-3.5-turbo'):
		self._gpt_token = os.getenv('GPT_TOKEN')
		self._proxy = os.getenv('PROXY')
		
		if not self._gpt_token:
			raise ConfigurationError("GPT_TOKEN environment variable is not set")
		
		self._client = self._create_client()
		self._model = model
	
	def _create_client(self):
		"""
		Создает экземпляр клиента AsyncOpenAI.
		:return: Экземпляр AsyncOpenAI
		:raises: APIConnectionError при сбое создания клиента
		"""
		try:
			gpt_client = openai.AsyncClient(
				api_key=self._gpt_token,
				http_client=httpx.AsyncClient(
					proxy=self._proxy,
					timeout=30.0  # Add timeout
				)
			)
			return gpt_client
		except Exception as e:
			raise APIConnectionError(f"Failed to create OpenAI client: {str(e)}")
	
	async def request(self, message: GPTMessage):
		"""
		Получает ответ от модели ChatGPT на основе предоставленных сообщений.
		:param message: Объект GPTMessage, содержащий список сообщений
		:return: Ответ модели ChatGPT в виде строки
		:raises: APIConnectionError при сбое запроса API
		"""
		try:
			response = await self._client.chat.completions.create(
				messages=message.message_list,
				model=self._model,
			)
			if not response.choices:
				raise APIConnectionError("No response received from the API")
			return response.choices[0].message.content
		except openai.APIError as e:
			raise APIConnectionError(f"OpenAI API error: {str(e)}")
		except httpx.RequestError as e:
			raise APIConnectionError(f"Network error: {str(e)}")
		except Exception as e:
			raise APIConnectionError(f"Unexpected error during API request: {str(e)}")
