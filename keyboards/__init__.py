"""
Пакет клавиатур для Telegram бота.

Этот пакет содержит все клавиатуры и кнопки, используемые
в интерфейсе Telegram бота для взаимодействия с пользователями.

Содержит:
- kb_replay: Обычная клавиатура с кнопками повтора
- kb_end_talk: Клавиатура для завершения разговора со знаменитостью
- kb_end_gpt: Клавиатура для завершения разговора с ChatGPT
- ikb_celebrity: Inline клавиатура для выбора знаменитости
- ikb_quiz_select_topic: Inline клавиатура для выбора темы викторины
- ikb_quiz_next: Inline клавиатура для навигации в викторине
- ikb_translator: Inline клавиатура для выбора направления перевода

Экспортирует:
- Все клавиатуры для импорта в других модулях
"""

from .keyboards import kb_replay, kb_end_talk, kb_end_gpt
from .inline_keyboards import ikb_celebrity, ikb_quiz_select_topic, ikb_quiz_next, ikb_translator, ikb_media_actions, ikb_media_genres, ikb_media_categories

__all__ = [
	'kb_replay',
	'kb_end_talk',
	'kb_end_gpt',
	'ikb_celebrity',
	'ikb_quiz_select_topic',
	'ikb_quiz_next',
	'ikb_translator',
	'ikb_media_actions',
	'ikb_media_genres',
	'ikb_media_categories'
]
