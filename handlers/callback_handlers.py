from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging

from classes import gpt_client
from classes.callback_data import CelebrityData, QuizData, TranslatorData
from classes.resource import Resource
from classes.buttons import Button
from classes.enum_path import GPTRole
from classes.chat_gpt import GPTMessage, GPTError, APIConnectionError
from .state_handlers import CelebrityTalk, Quiz, Translator
from commands.commands import cmd_start, cmd_quiz
from misc import bot_thinking

logger = logging.getLogger(__name__)
callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
	try:
		photo = Resource(callback_data.file_name).photo
		button_name = Button(callback_data.file_name).name
		await callback.answer(
			text=f'С тобой говорит {button_name}',
		)
		await bot.send_photo(
			chat_id=callback.from_user.id,
			photo=photo,
			caption=f'Задайте свой вопрос',
		)
		request_message = GPTMessage(callback_data.file_name)
		await state.set_state(CelebrityTalk.wait_for_answer)
		await state.set_data({'messages': request_message, 'photo': photo})
	except Exception as e:
		logger.error(f"Error in celebrity_callbacks: {str(e)}")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)


@callback_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def quiz_callbacks(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
	try:
		photo = Resource('quiz').photo
		await callback.answer(
			text=f'Вы выбрали тему {callback_data.topic_name}!',
		)
		request_message = GPTMessage('quiz')
		request_message.update(GPTRole.USER, callback_data.topic)
		
		try:
			response = await gpt_client.request(request_message)
		except APIConnectionError as e:
			logger.error(f"API error in quiz_callbacks: {str(e)}")
			await callback.answer("Извините, произошла ошибка при загрузке вопроса. Попробуйте позже.", show_alert=True)
			return
			
		await bot.send_photo(
			chat_id=callback.from_user.id,
			photo=photo,
			caption=response,
		)
		await state.set_state(Quiz.wait_for_answer)
		await state.set_data({'messages': request_message, 'photo': photo, 'score': 0, 'callback': callback_data})
	except Exception as e:
		logger.error(f"Error in quiz_callbacks: {str(e)}")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)


@callback_router.callback_query(Quiz.wait_press_button, QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, state: FSMContext) -> None:
	try:
		await callback.answer()
		await state.set_state(Quiz.wait_for_answer)
		
		data: dict[str, GPTMessage | str | QuizData] = await state.get_data()
		data['messages'].update(GPTRole.USER, 'quiz_more')
		
		try:
			response = await gpt_client.request(data['messages'])
		except APIConnectionError as e:
			logger.error(f"API error in quiz_next_question: {str(e)}")
			await callback.answer("Извините, произошла ошибка при загрузке следующего вопроса. Попробуйте позже.", show_alert=True)
			return
			
		data['messages'].update(GPTRole.ASSISTANT, response)
		await callback.bot.send_photo(
			chat_id=callback.from_user.id,
			photo=data['photo'],
			caption=response,
			parse_mode=None,
		)
		await callback.answer(
			text=f'Продолжаем тему {data['callback'].topic_name}'
		)
		await state.update_data(data)
	except Exception as e:
		logger.error(f"Error in quiz_next_question: {str(e)}")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)


@callback_router.callback_query(QuizData.filter(F.button == 'change_topic'))
async def quiz_change_topic(callback: CallbackQuery, state: FSMContext) -> None:
	try:
		await callback.answer()
		message = callback.message
		await bot_thinking(message)
		await state.clear()
		await cmd_quiz(message, state)
	except Exception as e:
		logger.error(f"Error in quiz_change_topic: {str(e)}")
		await callback.answer("Произошла ошибка при смене темы. Попробуйте еще раз.", show_alert=True)


@callback_router.callback_query(QuizData.filter(F.button == 'finish_quiz'))
async def quiz_finish(callback: CallbackQuery, state: FSMContext) -> None:
	try:
		await callback.answer()
		message = callback.message
		await bot_thinking(message)
		await state.clear()
		await cmd_start(message)
	except Exception as e:
		logger.error(f"Error in quiz_finish: {str(e)}")
		await callback.answer("Произошла ошибка при завершении квиза. Попробуйте еще раз.", show_alert=True)

@callback_router.callback_query(Translator.select_direction, TranslatorData.filter())
async def translator_direction_callback(callback: CallbackQuery, callback_data: TranslatorData, state: FSMContext):
	"""
	Обрабатывает выбор направления перевода и устанавливает состояние ожидания текста.

	:param callback: CallbackQuery объект
	:param callback_data: Данные callback с выбранным направлением перевода
	:param state: Контекст состояния
	:return: None
	"""
	try:
		await callback.answer()
		await state.set_state(Translator.wait_for_text)
		await state.set_data({'direction': callback_data.button})
		
		direction_text = "английского на русский" if callback_data.button == "eng_rus" else "русского на английский"
		await callback.message.answer(f"Введите текст для перевода с {direction_text}:")
	except Exception as e:
		logger.error(f"Error in translator_direction_callback: {str(e)}")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)
