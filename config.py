"""
Модуль конфигурации приложения.

Содержит настройки и константы для Telegram бота,
включая токены, модели GPT и другие параметры.

Основные компоненты:
- Config: Класс для управления конфигурацией приложения
"""

import os
from typing import Optional


class Config:
    """
    Класс для управления конфигурацией приложения.
    
    Содержит все настройки приложения, включая токены, модели,
    сетевые параметры и настройки логирования.
    """
    
    # Telegram Bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    
    # OpenAI
    GPT_TOKEN: str = os.getenv('GPT_TOKEN', '')
    GPT_MODEL: str = os.getenv('GPT_MODEL', 'gpt-3.5-turbo')
    
    # Network
    PROXY: Optional[str] = os.getenv('PROXY')
    REQUEST_TIMEOUT: float = 30.0
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate(cls) -> None:
        """
        Проверяет корректность конфигурации.
        
        Raises:
            ValueError: Если обязательные параметры не установлены
        """
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is not set")
        if not cls.GPT_TOKEN:
            raise ValueError("GPT_TOKEN environment variable is not set")
    
    @classmethod
    def get_logging_config(cls) -> dict:
        """
        Возвращает конфигурацию логирования.
        
        Returns:
            dict: Настройки логирования с ключами 'level' и 'format'
        """
        return {
            'level': cls.LOG_LEVEL,
            'format': cls.LOG_FORMAT
        } 