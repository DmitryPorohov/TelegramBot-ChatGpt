"""
Общий пакет приложения.

Содержит все общие компоненты приложения:
- Константы и перечисления
- Работа с ресурсами
- Типы данных
- Утилиты

Основные экспорты:
- MESSAGES, ERROR_CODES, LIMITS: Константы приложения
- ResourcePath, GPTRole, Extensions, MediaCategory, MediaGenre, TranslationDirection: Перечисления
- MEDIA_CATEGORY_NAMES, MEDIA_GENRE_NAMES, MEDIA_GENRES_BY_CATEGORY, TRANSLATION_DIRECTION_TEXTS: Словари данных
- Resource: Класс для работы с ресурсами

Пример использования:
    from common import Resource, MediaCategory, MESSAGES
"""

# Импорты для удобного доступа к основным компонентам
from .constants import MESSAGES, ERROR_CODES, LIMITS
from .enums import (
    ResourcePath, GPTRole, Extensions, MediaCategory, MediaGenre, TranslationDirection,
    MEDIA_CATEGORY_NAMES, MEDIA_GENRE_NAMES, MEDIA_GENRES_BY_CATEGORY, TRANSLATION_DIRECTION_TEXTS
)
from .assets import Resource

# Экспорт основных компонентов
__all__ = [
    # Константы
    'MESSAGES', 'ERROR_CODES', 'LIMITS',
    
    # Перечисления
    'ResourcePath', 'GPTRole', 'Extensions', 'MediaCategory', 'MediaGenre', 'TranslationDirection',
    
    # Словари данных
    'MEDIA_CATEGORY_NAMES', 'MEDIA_GENRE_NAMES', 'MEDIA_GENRES_BY_CATEGORY', 'TRANSLATION_DIRECTION_TEXTS',
    
    # Классы
    'Resource',
] 