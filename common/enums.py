"""
Модуль с перечислениями и константами приложения.

Объединяет все перечисления и связанные константы в одном месте
для удобства управления и избежания дублирования.

Содержит:
- ResourcePath: Пути к различным типам ресурсов
- GPTRole: Роли в диалоге с GPT
- Extensions: Расширения файлов
- MediaCategory: Категории медиа
- MediaGenre: Жанры медиа
- TranslationDirection: Направления перевода

А также словари для удобного доступа к данным:
- MEDIA_CATEGORY_NAMES: Названия категорий медиа
- MEDIA_GENRE_NAMES: Названия жанров медиа
- MEDIA_GENRES_BY_CATEGORY: Жанры по категориям
- TRANSLATION_DIRECTION_TEXTS: Тексты направлений перевода
"""

from enum import Enum
import os
from typing import Dict, List


class ResourcePath(Enum):
    """Перечисление путей к ресурсам приложения."""
    RESOURCES = 'resources'
    IMAGES = os.path.join(RESOURCES, 'images')
    MESSAGES = os.path.join(RESOURCES, 'messages')
    PROMPTS = os.path.join(RESOURCES, 'prompts')


class GPTRole(Enum):
    """Перечисление ролей в диалоге с GPT."""
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class Extensions(Enum):
    """Перечисление расширений файлов."""
    JPG = '.jpg'
    TXT = '.txt'
    JSON = '.json'


class MediaCategory(Enum):
    """Перечисление категорий медиа."""
    MOVIES = 'movies'
    BOOKS = 'books'
    MUSIC = 'music'


class MediaGenre(Enum):
    """Перечисление жанров медиа."""
    # Фильмы
    ACTION = 'action'
    COMEDY = 'comedy'
    DRAMA = 'drama'
    HORROR = 'horror'
    SCI_FI = 'sci-fi'
    THRILLER = 'thriller'
    
    # Книги
    FANTASY = 'fantasy'
    DETECTIVE = 'detective'
    NOVEL = 'novel'
    ADVENTURE = 'adventure'
    HISTORICAL = 'historical'
    SCIENCE = 'science'
    
    # Музыка
    ROCK = 'rock'
    POP = 'pop'
    CLASSICAL = 'classical'
    JAZZ = 'jazz'
    ELECTRONIC = 'electronic'
    FOLK = 'folk'


class TranslationDirection(Enum):
    """Перечисление направлений перевода."""
    ENG_RUS = 'eng_rus'
    RUS_ENG = 'rus_eng'


# Словари для удобного доступа к данным
MEDIA_CATEGORY_NAMES: Dict[MediaCategory, str] = {
    MediaCategory.MOVIES: 'Фильмы',
    MediaCategory.BOOKS: 'Книги',
    MediaCategory.MUSIC: 'Музыка',
}

MEDIA_GENRE_NAMES: Dict[MediaGenre, str] = {
    # Фильмы
    MediaGenre.ACTION: 'Боевик',
    MediaGenre.COMEDY: 'Комедия',
    MediaGenre.DRAMA: 'Драма',
    MediaGenre.HORROR: 'Ужасы',
    MediaGenre.SCI_FI: 'Фантастика',
    MediaGenre.THRILLER: 'Триллер',
    
    # Книги
    MediaGenre.FANTASY: 'Фэнтези',
    MediaGenre.DETECTIVE: 'Детектив',
    MediaGenre.NOVEL: 'Роман',
    MediaGenre.ADVENTURE: 'Приключения',
    MediaGenre.HISTORICAL: 'Исторический',
    MediaGenre.SCIENCE: 'Научная литература',
    
    # Музыка
    MediaGenre.ROCK: 'Рок',
    MediaGenre.POP: 'Поп',
    MediaGenre.CLASSICAL: 'Классика',
    MediaGenre.JAZZ: 'Джаз',
    MediaGenre.ELECTRONIC: 'Электроника',
    MediaGenre.FOLK: 'Фолк',
}

MEDIA_GENRES_BY_CATEGORY: Dict[MediaCategory, List[MediaGenre]] = {
    MediaCategory.MOVIES: [
        MediaGenre.ACTION, MediaGenre.COMEDY, MediaGenre.DRAMA,
        MediaGenre.HORROR, MediaGenre.SCI_FI, MediaGenre.THRILLER
    ],
    MediaCategory.BOOKS: [
        MediaGenre.FANTASY, MediaGenre.DETECTIVE, MediaGenre.NOVEL,
        MediaGenre.ADVENTURE, MediaGenre.HISTORICAL, MediaGenre.SCIENCE
    ],
    MediaCategory.MUSIC: [
        MediaGenre.ROCK, MediaGenre.POP, MediaGenre.CLASSICAL,
        MediaGenre.JAZZ, MediaGenre.ELECTRONIC, MediaGenre.FOLK
    ],
}

TRANSLATION_DIRECTION_TEXTS: Dict[TranslationDirection, str] = {
    TranslationDirection.ENG_RUS: 'английского на русский',
    TranslationDirection.RUS_ENG: 'русского на английский',
} 