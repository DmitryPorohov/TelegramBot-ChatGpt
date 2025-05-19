from .commands import command_router
from .callback_handlers import callback_router
from aiogram import Router
from .message_handler import messages_router

main_router = Router()
main_router.include_routers(
messages_router,
	command_router,
	callback_router,
)
__all__ = [
	'main_router',
]
