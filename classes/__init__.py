from .chat_gpt import ChatGpt

gpt_client = ChatGpt()
__all__ = [
	'ChatGpt',
	'gpt_client',
]
