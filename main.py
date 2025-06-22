"""
Главный модуль Telegram бота с интеграцией ChatGPT.

Этот модуль содержит основную логику запуска и настройки Telegram бота,
включая конфигурацию логирования, обработку ошибок и инициализацию
основных компонентов приложения.

Основные функции:
- get_bot_token(): Получение токена бота из конфигурации
- start_bot(): Запуск и настройка бота с обработчиками
- main(): Главная функция приложения

Зависимости:
- aiogram: Фреймворк для создания Telegram ботов
- asyncio: Асинхронное программирование
- logging: Система логирования
- config: Конфигурация приложения
- exception: Пользовательские исключения
- handlers: Обработчики сообщений и команд
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

from handlers import routers
from config import Config
from exception import ConfigurationError, log_exception

# Настройка логирования
logging_config = Config.get_logging_config()
logging.basicConfig(
    level=getattr(logging, logging_config['level']),
    format=logging_config['format']
)
logger = logging.getLogger(__name__)


def get_bot_token() -> str:
    """
    Получение токена бота из конфигурации.
    
    Returns:
        str: Токен бота для подключения к Telegram API
        
    Raises:
        ConfigurationError: Если токен не установлен
    """
    if not Config.BOT_TOKEN:
        raise ConfigurationError("BOT_TOKEN environment variable is not set")
    return Config.BOT_TOKEN


async def start_bot():
    """
    Запуск и настройка Telegram бота.
    
    Инициализирует бота с настройками по умолчанию, создает диспетчер,
    подключает все роутеры и запускает поллинг для получения обновлений.
    
    Raises:
        ConfigurationError: При ошибках конфигурации
        TelegramAPIError: При ошибках Telegram API
        Exception: При других неожиданных ошибках
    """
    try:
        # Валидация конфигурации
        Config.validate()
        
        bot = Bot(
            token=get_bot_token(),
            default=DefaultBotProperties(
                parse_mode=ParseMode.MARKDOWN,
            )
        )
        dp = Dispatcher()
        dp.include_routers(*routers)
        
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    except ConfigurationError as e:
        log_exception(e, "Configuration error")
        raise
    except TelegramAPIError as e:
        log_exception(e, "Telegram API error")
        raise
    except Exception as e:
        log_exception(e, "Unexpected error")
        raise


def main():
    """
    Главная функция приложения.
    
    Запускает бота в асинхронном режиме с обработкой различных типов ошибок
    и корректным завершением работы при получении сигнала прерывания.
    """
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except ConfigurationError as e:
        log_exception(e, "Configuration error")
    except TelegramAPIError as e:
        log_exception(e, "Telegram API error")
    except Exception as e:
        log_exception(e, "Unexpected error")
    finally:
        logger.info("Bot stopped")


if __name__ == '__main__':
    main()
