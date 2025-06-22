"""
Модуль для обработки callback-запросов.

Содержит функции для обработки нажатий на инлайн-кнопки:
- handle_translation_callback: Обработка выбора направления перевода
- handle_quiz_callback: Обработка ответов в викторине
- handle_media_callback: Обработка выбора категорий и жанров медиа
- handle_gpt_callback: Обработка диалога с GPT
- handle_celebrity_callback: Обработка разговора со знаменитостями

Зависимости:
- aiogram: Фреймворк для Telegram ботов
- models: Модели данных
- core: Основные компоненты приложения
- keyboards: Inline клавиатуры
- commands: Команды бота
- utils: Вспомогательные функции
- exception: Обработка исключений
"""

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, InputFileUnion, Message
import logging
from typing import cast, Optional, Dict, Any, TypedDict
import asyncio

from models import ChatGpt, GPTMessage, GPTRole, MediaData, CelebrityData, QuizData, TranslatorData, QuizStateData, MediaStateData, Button
from common import Resource
from keyboards import ikb_media_genres, ikb_media_actions
from handlers.state_handlers import MediaRecommendation, CelebrityTalk, Quiz, Translator
from commands import cmd_start, cmd_quiz
from utils import bot_thinking
from exception import APIConnectionError, log_exception

logger = logging.getLogger(__name__)
callback_router = Router()
gpt_client = ChatGpt()


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
		log_exception(e, "Error in celebrity_callbacks")
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
			log_exception(e, "API error in quiz_callbacks")
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
		log_exception(e, "Error in quiz_callbacks")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)


@callback_router.callback_query(Quiz.wait_press_button, QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, state: FSMContext) -> None:
	try:
		await callback.answer()
		await state.set_state(Quiz.wait_for_answer)
		
		data = cast(QuizStateData, await state.get_data())
		messages = cast(GPTMessage, data['messages'])
		messages.update(GPTRole.USER, 'quiz_more')
		
		try:
			response = await gpt_client.request(messages)
		except APIConnectionError as e:
			log_exception(e, "API error in quiz_next_question")
			await callback.answer("Извините, произошла ошибка при загрузке следующего вопроса. Попробуйте позже.", show_alert=True)
			return
			
		messages.update(GPTRole.ASSISTANT, response)
		photo = cast(FSInputFile, data['photo'])
		callback_data = cast(QuizData, data['callback'])
		
		await callback.bot.send_photo(
			chat_id=callback.from_user.id,
			photo=cast(InputFileUnion, photo),
			caption=response,
			parse_mode=None,
		)
		await callback.answer(
			text=f'Продолжаем тему {callback_data.topic_name}'
		)
		await state.update_data(data)
	except Exception as e:
		log_exception(e, "Error in quiz_next_question")
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
		log_exception(e, "Error in quiz_change_topic")
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
		log_exception(e, "Error in quiz_finish")
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
		log_exception(e, "Error in translator_direction_callback")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)


def get_media_photo() -> Optional[FSInputFile]:
	"""Вспомогательная функция для получения фотографии в виде FSInputFile"""
	resource = Resource('media')
	photo = resource.photo
	if photo and isinstance(photo, FSInputFile):
		return photo
	return None

@callback_router.callback_query(MediaRecommendation.select_category, MediaData.filter(F.button == 'select_category'))
async def media_select_category(callback: CallbackQuery, callback_data: MediaData, state: FSMContext):
	"""
	Обрабатывает выбор категории медиа (фильмы, книги, музыка).
	"""
	try:
		await callback.answer()
		await state.set_state(MediaRecommendation.select_genre)
		await state.update_data({'category': callback_data.category, 'disliked': []})
		
		photo = get_media_photo()
		if photo and callback.message:
			media = InputMediaPhoto(
				media=cast(InputFileUnion, photo),
				caption=f'Вы выбрали категорию: *{callback_data.category}*\nТеперь выберите жанр:',
			)
			message = cast(Message, callback.message)
			await message.edit_media(
				media=media,
				reply_markup=ikb_media_genres(callback_data.category)
			)
		elif callback.message:
			message = cast(Message, callback.message)
			await message.edit_caption(
				caption=f'Вы выбрали категорию: *{callback_data.category}*\nТеперь выберите жанр:',
				reply_markup=ikb_media_genres(callback_data.category)
			)
	except Exception as e:
		log_exception(e, "Error in media_select_category")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)

@callback_router.callback_query(MediaRecommendation.select_genre, MediaData.filter(F.button == 'select_genre'))
async def media_select_genre(callback: CallbackQuery, callback_data: MediaData, state: FSMContext):
	"""
	Обрабатывает выбор жанра и отправляет запрос рекомендации.
	"""
	try:
		await callback.answer()
		await state.set_state(MediaRecommendation.wait_for_recommendation)
		data: Dict[str, Any] = await state.get_data()
		
		# Формируем запрос к ChatGPT
		user_query = f'Категория: {callback_data.category}\nЖанр: {callback_data.genre}'
		if data.get('disliked'):
			user_query += f"\nНе предлагай: {', '.join(data['disliked'])}"
			
		gpt_message = GPTMessage('media')
		gpt_message.update(GPTRole.USER, user_query)
		
		try:
			response = await gpt_client.request(gpt_message)
		except APIConnectionError as e:
			log_exception(e, "API error in media_select_genre")
			await callback.answer("Извините, произошла ошибка при получении рекомендации. Попробуйте позже.", show_alert=True)
			return
			
		# Парсим ответ и сохраняем данные
		rec = parse_media_response(response)
		photo = get_media_photo()
		if photo and callback.message:
			state_data: MediaStateData = {
				'category': callback_data.category,
				'genre': callback_data.genre,
				'last_rec': rec,
				'disliked': data.get('disliked', []),
				'messages': gpt_message,
				'photo': photo
			}
			await state.update_data(state_data)
			
			# Отправляем рекомендацию
			message = cast(Message, callback.message)
			await message.delete()
			caption = f"*{rec['title']}*\n_{rec['desc']}_"
			
			await message.answer_photo(
				photo=cast(InputFileUnion, photo),
				caption=caption,
				reply_markup=ikb_media_actions(callback_data.category, callback_data.genre)
			)
		elif callback.message:
			message = cast(Message, callback.message)
			await message.answer(
				text=f"*{rec['title']}*\n_{rec['desc']}_",
				reply_markup=ikb_media_actions(callback_data.category, callback_data.genre)
			)
	except Exception as e:
		log_exception(e, "Error in media_select_genre")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)

@callback_router.callback_query(MediaRecommendation.wait_for_recommendation, MediaData.filter(F.button == 'dislike'))
async def media_dislike(callback: CallbackQuery, callback_data: MediaData, state: FSMContext):
	"""
	Обрабатывает нажатие кнопки "Не нравится" и предлагает новую рекомендацию.
	"""
	try:
		await callback.answer('Генерирую новую рекомендацию...')
		data = cast(MediaStateData, await state.get_data())
		
		# Добавляем текущую рекомендацию в список нежелательных
		disliked = data['disliked']
		last_rec = data['last_rec']
		if last_rec.get('title'):
			disliked.append(last_rec['title'])
		
		# Запрашиваем новую рекомендацию
		user_query = f'Категория: {callback_data.category}\nЖанр: {callback_data.genre}'
		if disliked:
			user_query += f"\nНе предлагай: {', '.join(disliked)}"
			
		gpt_message = GPTMessage('media')
		gpt_message.update(GPTRole.USER, user_query)
		
		try:
			response = await gpt_client.request(gpt_message)
		except APIConnectionError as e:
			log_exception(e, "API error in media_dislike")
			await callback.answer("Извините, произошла ошибка при получении новой рекомендации. Попробуйте позже.", show_alert=True)
			return
			
		# Обновляем данные и отправляем новую рекомендацию
		rec = parse_media_response(response)
		photo = get_media_photo()
		if photo and callback.message:
			state_data: MediaStateData = {
				'category': callback_data.category,
				'genre': callback_data.genre,
				'last_rec': rec,
				'disliked': disliked,
				'messages': gpt_message,
				'photo': photo
			}
			await state.update_data(state_data)
			
			message = cast(Message, callback.message)
			await message.delete()
			caption = f"*{rec['title']}*\n_{rec['desc']}_"
			
			await message.answer_photo(
				photo=cast(InputFileUnion, photo),
				caption=caption,
				reply_markup=ikb_media_actions(callback_data.category, callback_data.genre)
			)
		elif callback.message:
			message = cast(Message, callback.message)
			await message.answer(
				text=f"*{rec['title']}*\n_{rec['desc']}_",
				reply_markup=ikb_media_actions(callback_data.category, callback_data.genre)
			)
	except Exception as e:
		log_exception(e, "Error in media_dislike")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)

@callback_router.callback_query(MediaRecommendation.wait_for_recommendation, MediaData.filter(F.button == 'finish'))
async def media_finish(callback: CallbackQuery, state: FSMContext):
	"""
	Завершает сессию рекомендаций и возвращает в главное меню.
	"""
	try:
		await callback.answer('Спасибо за использование рекомендаций!')
		await state.clear()
		if callback.message:
			message = cast(Message, callback.message)
			await message.delete()
			await cmd_start(message)
	except Exception as e:
		log_exception(e, "Error in media_finish")
		await callback.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)

def parse_media_response(response: str) -> Dict[str, str]:
	"""
	Парсит ответ от ChatGPT в формате:
	Название: ...
	Описание: ...
	"""
	lines = response.strip().split('\n')
	result: Dict[str, str] = {'title': '', 'desc': ''}
	
	for line in lines:
		if line.startswith('Название:'):
			result['title'] = line.replace('Название:', '').strip()
		elif line.startswith('Описание:'):
			result['desc'] = line.replace('Описание:', '').strip()
			
	return result
