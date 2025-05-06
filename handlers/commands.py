import openai
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import os
from classes import gpt_client

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
	photo = FSInputFile(photo_path)
	buttons = [
		'Хочу ещё факт',
		'Закончить',
	]
	msg_text = await gpt_client.text_request('random')
	await message.answer_photo(
		photo=photo,
		caption=msg_text,
		reply_markup=kb_replay(buttons),
	)
