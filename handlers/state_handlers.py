from aiogram.fsm.state import State, StatesGroup


class ChatGPTRequests(StatesGroup):
	wait_for_request = State()


class CelebrityTalk(StatesGroup):
	wait_for_answer = State()


class Quiz(StatesGroup):
	wait_for_answer = State()
	select_topic = State()
	wait_press_button = State()


class Translator(StatesGroup):
	select_direction = State()
	wait_for_text = State()
