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
	
	def _init_message(self, prompt_name: str) -> dict[str, str | list[dict[str, str]]]:
		return {'messages': [
			{
				'role': 'system',
				'content': self._load_prompt(prompt_name),
			}
		],
			'model': 'gpt-3.5-turbo',
		}
	
	@staticmethod
	def _load_prompt(prompt_name: str)-> str:
		prompt_path = os.path.join('resources', 'prompts', f'{prompt_name}.txt')
		with open(prompt_path, 'r', encoding='UTF-8') as file:
			prompt = file.read()
		return prompt
	
	async def random_request(self):
		respons = await self._client.chat.completions.create(
			** self._init_message('random')
		)
		return respons.choices[0].message.content
		
	async def gpt_request(self, request_text: str) -> str:
		key_args = self._init_message('gpt')
		key_args['messages'].append(
			{
				'role': 'user',
				'content': request_text,
			}
		)
		respons = await self._client.chat.completions.create(
			**key_args,
		)
		return respons.choices[0].message.content