from aiogram.fsm.state import State,StatesGroup

class ChatGPTRequests (StatesGroup):
	wait_for_request = State()


class CelebrityTalk(StatesGroup):
	wait_for_answer = State()