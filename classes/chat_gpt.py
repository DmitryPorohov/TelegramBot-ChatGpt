import os

import openai
import httpx

class ChatGpt:
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance
	
	def __init__(self):
		self._gpt_token = os.getenv('GPT_TOKEN')
		self._proxy = os.getenv('PROXY')
		self._client = self._create_client()
		

	def _create_client(self):
		gpt_client = openai.AsyncClient(
			api_key=self._gpt_token,
			http_client=httpx.AsyncClient(
				proxy=self._proxy,
			)
		)
		return gpt_client
	
	@staticmethod
	def _load_prompt(prompt_name: str)-> str:
		prompt_path = os.path.join('resources', 'prompts', f'{prompt_name}.txt')
		with open(prompt_path, 'r', encoding='UTF-8') as file:
			prompt = file.read()
		return prompt
	
	async def text_request(self,prompt_name: str):
		respons = await self._client.chat.completions.create(
			messages=[
				{
					'role': 'system',
					'content': self._load_prompt(prompt_name),
				}
			],
			model='gpt-3.5-turbo',
		)
		return respons.choices[0].message.content
