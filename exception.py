"""
Модуль для пользовательских исключений и логирования ошибок Telegram бота.

Содержит:
- GPTError: Базовое исключение для ошибок, связанных с GPT
- FileOperationError: Исключение для ошибок файловой операции
- APIConnectionError: Исключение для ошибок подключения к API
- ConfigurationError: Исключение, вызванное ошибками конфигурации
- log_exception: Функция для логирования ошибок
"""

import logging

logger = logging.getLogger(__name__)


class GPTError(Exception):
    """Базовое исключение для ошибок, связанных с GPT."""
    pass


class FileOperationError(GPTError):
    """Исключение для ошибок файловой операции."""
    pass


class APIConnectionError(GPTError):
    """Исключение для ошибок подключения к API."""
    pass


class ConfigurationError(GPTError):
    """Исключение, вызванное ошибками конфигурации."""
    pass


def log_exception(error: Exception, context: str = ""):
    """
    Логирует ошибку с дополнительным контекстом.
    
    Args:
        error (Exception): Исключение для логирования
        context (str): Описание места возникновения ошибки
    """
    if context:
        logger.error(f"{context}: {str(error)}")
    else:
        logger.error(str(error)) 