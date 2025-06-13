from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import gpt_client
from classes.enum_path import GPTRole
from classes.resource import Resource
from classes.chat_gpt import GPTMessage

from .state_handlers import CelebrityTalk, ChatGPTRequests, Quiz

from keyboards import kb_end_talk, ikb_quiz_next
from classes.callback_data import QuizData
from commands.commands import cmd_start
from misc import bot_thinking

messages_router = Router()


@messages_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
	await state.clear()
	await cmd_start(message)


@messages_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, state: FSMContext):
	await bot_thinking(message)
	gpt_message = GPTMessage('gpt')
	gpt_message.update(GPTRole.USER, message.text)
	gpt_response = await gpt_client.request(gpt_message)
	photo = Resource('gpt').photo
	await message.answer_photo(
		photo=photo,
		caption=gpt_response,
	)
	await state.clear()


@messages_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
	await bot_thinking(message)
	data: dict[str, GPTMessage | str] = await state.get_data()
	data['messages'].update(GPTRole.USER, message.text)
	response = await gpt_client.request(data['messages'])
	await message.answer_photo(
		photo=data['photo'],
		caption=response,
		reply_markup=kb_end_talk(),
	)
	data['messages'].update(GPTRole.ASSISTANT, response)
	await state.update_data(data)


@messages_router.message(Quiz.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
	await bot_thinking(message)
	await state.set_state(Quiz.wait_for_answer)
	
	current_state = await state.get_data()
	data: dict[str, GPTMessage | str | QuizData] = current_state
	data['messages'].update(GPTRole.USER, message.text)
	
	response = await gpt_client.request(data['messages'])
	if 'Правильно!'.lower() in response.lower() and 'Неправильно!'.lower() not in response.lower():
		data['score'] += 1
	data['messages'].update(GPTRole.ASSISTANT, response)
	await state.update_data(data)
	await message.answer_photo(
		photo=data['photo'],
		caption=f'Ваш счет: {data['score']}\n{response}',
		reply_markup=ikb_quiz_next(data['callback']),
		parse_mode=None,
	)
	
	await state.set_state(Quiz.wait_press_button)
