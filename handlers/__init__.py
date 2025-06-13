from commands.commands import commands_router
from .callback_handlers import callback_router
from .message_handler import messages_router

routers = [
	messages_router,
	commands_router,
	callback_router,
]

__all__ = [
	'routers',
]
