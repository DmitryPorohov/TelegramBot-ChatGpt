from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from classes.chat_gpt import GPTMessage
from classes.resource import Resource
from handlers.state_handlers import ChatGPTRequests, Quiz, Translator
from misc import bot_thinking

from keyboards import kb_replay, ikb_celebrity, ikb_quiz_select_topic, ikb_translator

commands_router = Router()


@commands_router.message(F.text == 'Закончить')
@commands_router.message(Command('start'))
async def cmd_start(message: Message):
	"""
	Обрабатывает команду запуска и отправляет пользователю приветственное сообщение с кнопками меню.

	:param message: Сообщение, содержащее информацию о команде.
	:return: None
	"""
	resource = Resource('main')
	buttons = [
		'/random',
		'/gpt',
		'/talk',
		'/quiz',
		'/translator'
	]
	await message.answer_photo(
		**resource.as_kwargs(),
		reply_markup=kb_replay(buttons),
	)


@commands_router.message(F.text == 'Хочу ещё факт')
@commands_router.message(Command('random'))
async def cmd_random(message: Message):
	"""
	Обрабатывает команду для получения случайного факта.

	:param message: Сообщение, содержащее информацию о команде.
	:return: None
	"""
	await bot_thinking(message)
	resource = Resource('random')
	gpt_message = GPTMessage('random')
	buttons = [
		'Хочу ещё факт',
		'Закончить',
	]
	msg_text = await gpt_client.request(gpt_message)
	await message.answer_photo(
		photo=resource.photo,
		caption=msg_text,
		reply_markup=kb_replay(buttons),
	)


@commands_router.message(Command('gpt'))
async def cmd_gpt(message: Message, state: FSMContext):
	"""
	Обрабатывает команду для общения с ChatGPT, очищает состояние и устанавливает ожидание ответа.

	:param message: Сообщение, содержащее информацию о команде.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	await state.set_state(ChatGPTRequests.wait_for_request)
	await bot_thinking(message)
	resource = Resource('gpt')
	await message.answer_photo(
		**resource.as_kwargs(),
	)


@commands_router.message(Command('talk'))
async def cmd_talk(message: Message):
	"""
	Обрабатывает команду общения со знаменитостью и отправляет пользователю сообщение с фотографией.

	:param message: Сообщение, содержащее информацию о команде.
	:return: None
	"""
	await bot_thinking(message)
	resource = Resource('talk')
	await message.answer_photo(
		**resource.as_kwargs(),
		reply_markup=ikb_celebrity(),
	)


@commands_router.message(Command('quiz'))
async def cmd_quiz(message: Message, state: FSMContext):
	"""
	Обрабатывает команду квиза, устанавливает состояние и отправляет пользователю сообщение с фотографией.

	:param message: Сообщение, содержащее информацию о команде.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	await state.set_state(Quiz.select_topic)
	await bot_thinking(message)
	resource = Resource('quiz')
	await message.answer_photo(
		**resource.as_kwargs(),
		reply_markup=ikb_quiz_select_topic(),
	)


@commands_router.message(Command('translator'))
async def cmd_translator(message: Message, state: FSMContext):
	"""
	Обрабатывает команду переводчика и отправляет пользователю сообщение с выбором направления перевода.

	:param message: Сообщение, содержащее информацию о команде.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	await state.set_state(Translator.select_direction)
	await bot_thinking(message)
	resource = Resource('translator')
	await message.answer_photo(
		**resource.as_kwargs(),
		reply_markup=ikb_translator(),
	)
