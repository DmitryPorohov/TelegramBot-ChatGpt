from time import struct_time

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from classes import gpt_client
from keyboards.callback_data import CelebrityData
import os
from .handlers_state import CelebrityTalk

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
	photo_path = os.path.join('resources', 'images', callback_data.file_name+'.jpg')
	file_name = callback_data.file_name
	with open(os.path.join('resources', 'prompts', file_name + '.txt'), 'r', encoding='UTF-8') as file:
		celebrity_name = file.readline().split(', ')[0][5:]
	photo = FSInputFile(photo_path)
	await callback.answer(
		text=f'С тобой говорит {celebrity_name}',
	)
	await bot.send_photo(
		chat_id=callback.from_user.id,
		photo=photo,
		caption=f'Задайте свой вопрос',
	)
	init_message = gpt_client.init_message(file_name)['messages']
	
	await state.set_state(CelebrityTalk.wait_for_answer)
	await state.set_data({'messages': [init_message[0]], 'photo': photo})

	
