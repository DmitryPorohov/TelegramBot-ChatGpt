"""
Модуль команд для Telegram бота.

Содержит все команды бота, которые пользователи могут вызывать
через слэш-команды или текстовые кнопки в Telegram.

Основные команды:
- cmd_start: Главное меню бота
- cmd_random: Случайные факты
- cmd_gpt: Разговор с ChatGPT
- cmd_talk: Разговор со знаменитостями
- cmd_quiz: Викторина
- cmd_translator: Переводчик
- cmd_media: Рекомендации медиа

Основные возможности:
- Обработка команд пользователя
- Интеграция с ChatGPT API
- Управление состояниями FSM
- Отправка медиа-контента
- Навигация по функциям бота

Зависимости:
- aiogram: Фреймворк для Telegram ботов
- models: Модели данных
- common: Основные компоненты приложения
- handlers: Обработчики состояний
- keyboards: Клавиатуры и кнопки
- utils: Вспомогательные функции
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models import gpt_client, GPTMessage
from common import Resource
from handlers.state_handlers import ChatGPTRequests, Quiz, Translator, MediaRecommendation
from utils import bot_thinking

from keyboards import kb_replay, ikb_celebrity, ikb_quiz_select_topic, ikb_translator, ikb_media_categories

commands_router = Router()


@commands_router.message(F.text == 'Закончить')
@commands_router.message(Command('start'))
async def cmd_start(message: Message):
	"""
	Обрабатывает команду запуска и отправляет главное меню.
	
	Отправляет пользователю приветственное сообщение с фотографией
	и кнопками для навигации по функциям бота.
	
	Args:
		message (Message): Сообщение с командой /start или кнопкой "Закончить"
	"""
	resource = Resource('main')
	buttons = [
		'/random',
		'/gpt',
		'/talk',
		'/quiz',
		'/translator',
		'/media'
	]
	await message.answer_photo(
		photo=resource.photo,
		caption=resource.text,
		reply_markup=kb_replay(buttons),
	)


@commands_router.message(F.text == 'Хочу ещё факт')
@commands_router.message(Command('random'))
async def cmd_random(message: Message):
	"""
	Обрабатывает команду для получения случайного факта.
	
	Отправляет пользователю случайный интересный факт,
	полученный от ChatGPT, с возможностью запросить ещё.
	
	Args:
		message (Message): Сообщение с командой /random или кнопкой "Хочу ещё факт"
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
	Обрабатывает команду для общения с ChatGPT.
	
	Устанавливает состояние ожидания запроса от пользователя
	и отправляет приветственное сообщение для разговора с ChatGPT.
	
	Args:
		message (Message): Сообщение с командой /gpt
		state (FSMContext): Контекст состояния пользователя
	"""
	await state.set_state(ChatGPTRequests.wait_for_request)
	await bot_thinking(message)
	resource = Resource('gpt')
	await message.answer_photo(
		photo=resource.photo,
		caption=resource.text,
	)


@commands_router.message(Command('talk'))
async def cmd_talk(message: Message):
	"""
	Обрабатывает команду общения со знаменитостями.
	
	Отправляет пользователю сообщение с выбором знаменитости
	для начала диалога.
	
	Args:
		message (Message): Сообщение с командой /talk
	"""
	await bot_thinking(message)
	resource = Resource('talk')
	await message.answer_photo(
		photo=resource.photo,
		caption=resource.text,
		reply_markup=ikb_celebrity(),
	)


@commands_router.message(Command('quiz'))
async def cmd_quiz(message: Message, state: FSMContext):
	"""
	Обрабатывает команду запуска викторины.
	
	Устанавливает состояние выбора темы викторины и отправляет
	пользователю сообщение с выбором темы.
	
	Args:
		message (Message): Сообщение с командой /quiz
		state (FSMContext): Контекст состояния пользователя
	"""
	await state.set_state(Quiz.select_topic)
	await bot_thinking(message)
	resource = Resource('quiz')
	await message.answer_photo(
		photo=resource.photo,
		caption=resource.text,
		reply_markup=ikb_quiz_select_topic(),
	)


@commands_router.message(Command('translator'))
async def cmd_translator(message: Message, state: FSMContext):
	"""
	Обрабатывает команду запуска переводчика.
	
	Устанавливает состояние выбора направления перевода и отправляет
	пользователю сообщение с выбором языка.
	
	Args:
		message (Message): Сообщение с командой /translator
		state (FSMContext): Контекст состояния пользователя
	"""
	await state.set_state(Translator.select_direction)
	await bot_thinking(message)
	resource = Resource('translator')
	await message.answer_photo(
		photo=resource.photo,
		caption=resource.text,
		reply_markup=ikb_translator(),
	)


@commands_router.message(Command('media'))
async def cmd_media(message: Message, state: FSMContext):
	"""
	Обрабатывает команду запуска рекомендаций медиа.
	
	Устанавливает состояние выбора категории медиа и отправляет
	пользователю сообщение с выбором категории.
	
	Args:
		message (Message): Сообщение с командой /media
		state (FSMContext): Контекст состояния пользователя
	"""
	await state.set_state(MediaRecommendation.select_category)
	resource = Resource('media')
	await message.answer_photo(
		photo=resource.photo,
		caption=resource.text if resource.text is not None else '',
		reply_markup=ikb_media_categories()
	)
