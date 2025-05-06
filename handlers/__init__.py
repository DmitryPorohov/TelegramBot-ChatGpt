from .commands import command_router
from aiogram import Router

main_router = Router()
main_router.include_router(
	command_router,
)
__all__ = [
	'main_router',
]
