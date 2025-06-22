"""
Модуль с вспомогательными функциями.

Содержит утилитарные функции, используемые в различных частях приложения:
- bot_thinking: Показывает индикатор "печатает" во время обработки запроса
- format_score: Форматирует счет в читаемом виде
- truncate_text: Обрезает текст до указанной длины

Зависимости:
- aiogram: Фреймворк для Telegram ботов
- asyncio: Асинхронное программирование
"""

import asyncio
from aiogram.types import Message


async def bot_thinking(message: Message) -> None:
	"""
	Показывает индикатор "печатает" во время обработки запроса.
	
	Отправляет индикатор "печатает" на 1 секунду, чтобы показать
	пользователю, что бот обрабатывает его запрос.
	
	Args:
		message (Message): Сообщение пользователя
	"""
	if message.bot:
		await message.bot.send_chat_action(
			chat_id=message.chat.id,
			action="typing"
		)
	await asyncio.sleep(1)


def format_score(score: int, total: int) -> str:
    """
    Форматирует счет в читаемом виде.
    
    Args:
        score (int): Количество правильных ответов
        total (int): Общее количество вопросов
        
    Returns:
        str: Отформатированный счет в виде "score/total"
    """
    return f"{score}/{total}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Обрезает текст до указанной длины.
    
    Args:
        text (str): Исходный текст
        max_length (int): Максимальная длина (по умолчанию 100)
        
    Returns:
        str: Обрезанный текст с "..." в конце, если превышает лимит
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..." 