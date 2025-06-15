from datetime import datetime

from aiogram.enums import ChatAction
from aiogram.types import Message


async def bot_thinking(message: Message):
	await message.bot.send_chat_action(
		chat_id=message.from_user.id,
		action=ChatAction.TYPING,
	)
