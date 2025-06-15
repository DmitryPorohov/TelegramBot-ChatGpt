from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError
import logging

from classes import gpt_client
from classes.enum_path import GPTRole
from classes.resource import Resource
from classes.chat_gpt import GPTMessage, GPTError, APIConnectionError


from .state_handlers import CelebrityTalk, ChatGPTRequests, Quiz

from keyboards import kb_end_talk, ikb_quiz_next, kb_end_gpt
from classes.callback_data import QuizData
from commands.commands import cmd_start
from misc import bot_thinking

logger = logging.getLogger(__name__)
messages_router = Router()


@messages_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
	"""
	Завершает разговор со знаменитостью и очищает состояние пользователя.

	:param message: Сообщение от пользователя, содержащее запрос на завершение разговора.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	try:
		await state.clear()
		await cmd_start(message)
	except Exception as e:
		logger.error(f"Error in end_talk_handler: {str(e)}")
		await message.answer("Произошла ошибка при завершении разговора. Попробуйте еще раз.")


@messages_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
	"""
	Обрабатывает сообщения пользователя во время разговора со знаменитостью.

	:param message: Сообщение от пользователя, содержащее текст для отправки.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	try:
		await bot_thinking(message)
		data: dict[str, GPTMessage | str] = await state.get_data()
		data['messages'].update(GPTRole.USER, message.text)
		
		try:
			response = await gpt_client.request(data['messages'])
		except APIConnectionError as e:
			logger.error(f"API error in talk_handler: {str(e)}")
			await message.answer("Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже.")
			return
			
		await message.answer_photo(
			photo=data['photo'],
			caption=response,
			reply_markup=kb_end_talk(),
		)
		data['messages'].update(GPTRole.ASSISTANT, response)
		await state.update_data(data)
	except Exception as e:
		logger.error(f"Error in talk_handler: {str(e)}")
		await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.")


@messages_router.message(ChatGPTRequests.wait_for_request, F.text == 'Закончить')
async def end_gpt_handler(message: Message, state: FSMContext):
	"""
	Завершает разговор со ChatGpt и очищает состояние пользователя.

	:param message: Сообщение от пользователя, содержащее запрос на завершение разговора.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	try:
		await state.clear()
		await cmd_start(message)
	except Exception as e:
		logger.error(f"Error in end_gpt_handler: {str(e)}")
		await message.answer("Произошла ошибка при завершении разговора. Попробуйте еще раз.")


@messages_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, state: FSMContext):
	"""
	Обрабатывает сообщения, ожидая ответ от ChatGPT. Устанавливает состояние ожидания и обновляет данные состояния.

	:param message: Сообщение, содержащее текст от пользователя.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	try:
		await bot_thinking(message)
		await state.set_state(ChatGPTRequests.wait_for_request)
		
		photo = Resource('gpt').photo
		current_state = await state.get_data()
		if not current_state:
			request_message = GPTMessage('gpt')
			data: dict[str, GPTMessage | str] = {'messages': request_message, 'photo': photo}
		else:
			data: dict[str, GPTMessage | str] = current_state
			data['messages'].update(GPTRole.USER, message.text)
			
		try:
			response = await gpt_client.request(data['messages'])
		except APIConnectionError as e:
			logger.error(f"API error in wait_for_gpt_handler: {str(e)}")
			await message.answer("Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже.")
			return
			
		data['messages'].update(GPTRole.ASSISTANT, response)
		
		await state.update_data(data)
		await message.answer_photo(
			photo=photo,
			caption=response,
			reply_markup=kb_end_gpt(),
		)
	except Exception as e:
		logger.error(f"Error in wait_for_gpt_handler: {str(e)}")
		await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.")


@messages_router.message(Quiz.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
	"""
	Обрабатывает ответ на вопрос викторины, обновляет состояние и отправляет пользователю результат.

	:param message: Сообщение, содержащее ответ пользователя.
	:param state: Контекст состояния для управления состоянием пользователя.
	:return: None
	"""
	try:
		await bot_thinking(message)
		await state.set_state(Quiz.wait_for_answer)
		
		current_state = await state.get_data()
		data: dict[str, GPTMessage | str | QuizData] = current_state
		data['messages'].update(GPTRole.USER, message.text)
		
		try:
			response = await gpt_client.request(data['messages'])
		except APIConnectionError as e:
			logger.error(f"API error in quiz_answer: {str(e)}")
			await message.answer("Извините, произошла ошибка при обработке вашего ответа. Попробуйте позже.")
			return
			
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
	except Exception as e:
		logger.error(f"Error in quiz_answer: {str(e)}")
		await message.answer("Произошла ошибка при обработке вашего ответа. Попробуйте еще раз.")
