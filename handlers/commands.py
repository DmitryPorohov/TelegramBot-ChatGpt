import openai
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import os
import httpx
from openai.types.beta.threads.runs import ToolCallDeltaObject

from keyboards import kb_replay

command_router = Router()


@command_router.message(F.text == 'Закончить')
@command_router.message(Command('start'))
async def cmd_start(message: Message):
	photo_path = os.path.join('resources', 'images', 'main.jpg')
	text_path = os.path.join('resources', 'messages', 'main.txt')
	photo = FSInputFile(photo_path)
	buttons = [
		'/random',
		'/gpt',
		'/talk',
		'/quiz'
	]
	with open(text_path, 'r', encoding='UTF-8') as file:
		msg_text = file.read()
	await message.answer_photo(
		photo=photo,
		caption=msg_text,
		reply_markup=kb_replay(buttons),
	)


@command_router.message(F.text == 'Хочу ещё факт')
@command_router.message(Command('random'))
async def cmd_random(message: Message):
	photo_path = os.path.join('resources', 'images', 'random.jpg')
	prompt_path = os.path.join('resources', 'prompts', 'random.txt')
	with open(prompt_path, 'r', encoding='UTF-8') as file:
		prompt = file.read()
	gpt_client = openai.AsyncClient(
		api_key= os.getenv('GPT_TOKEN'),
		http_client=httpx.AsyncClient(
			proxy= os.getenv('PROXY'),
		)
	)
	msg_text = await gpt_client.chat.completions.create(
		messages=[
			{
				'role': 'system',
				'content': prompt,
			}
		],
		model= 'gpt-3.5-turbo',
	)
	photo = FSInputFile(photo_path)
	buttons = [
		'Хочу ещё факт',
		'Закончить',
	]
	await message.answer_photo(
		photo=photo,
		caption=msg_text.choices[0].message.content,
		reply_markup=kb_replay(buttons),
	)
