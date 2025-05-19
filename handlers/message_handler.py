from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from classes import gpt_client

from .handlers_state import CelebrityTalk
from keyboards import kb_end_talk
from .commands import cmd_start
messages_router = Router()

@messages_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state:FSMContext):
	await state.clear()
	await cmd_start(message)
 
 
@messages_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state:FSMContext):
	data= await state.get_data()
	message_from_user = {
		'role': 'user',
		'content': message.text,}
	data['messages'].append(message_from_user)
	response = await gpt_client.talk_request(data['messages'])
	await message.answer_photo(
		photo=data['photo'],
		caption=response,
		reply_markup=kb_end_talk(),
	)
	messages_from_celebrity = {
		'role': 'assistant',
		'content': response,
	}
	data['messages'].append(messages_from_celebrity)
	await state.update_data(data)
