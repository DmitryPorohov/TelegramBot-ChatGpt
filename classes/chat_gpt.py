import os
import openai
import httpx
from .enum_path import GPTRole, Extensions

from classes.enum_path import ResourcePath


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
		Открываем и читаем файл prompt
		:return: str -> содержимое файла prompt
		"""
		prompt_path = os.path.join(ResourcePath.PROMPTS.value, self.prompt_file)
		with open(prompt_path, 'r', encoding='UTF-8') as file:
			prompt = file.read()
		return prompt
	
	def update(self, role: GPTRole, message: str):
		"""
		Добавление в сообщение новой роли и дублирование старого собщения,
		для поддержания контекста
		"""
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
		self._client = self._create_client()
		self._model = model
	
	def _create_client(self):
		"""
		Создает экземпляр AsyncOpenAI клиента.

        :return: Экземпляр AsyncOpenAI.
		"""
		gpt_client = openai.AsyncClient(
			api_key=self._gpt_token,
			http_client=httpx.AsyncClient(
				proxy=self._proxy,
			)
		)
		return gpt_client
	
	async def request(self, message: GPTMessage):
		"""
		Получает ответ от модели ChatGPT на основе переданных сообщений.

		:param message: Объект GPTMessage, содержащий список сообщений.
		:return: Ответ модели ChatGPT в виде строки.
		"""
		response = await self._client.chat.completions.create(
			messages=message.message_list,
			model=self._model,
		)
		return response.choices[0].message.content
