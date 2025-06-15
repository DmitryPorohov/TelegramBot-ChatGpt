import asyncio
import misc
import os
import logging
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

from handlers import routers
from classes.chat_gpt import GPTError, ConfigurationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_bot_token() -> str:
    """
    Получение токена бота из переменных окружения
    :return: Bot token
    :raises: ConfigurationError, если токен не установлен
    """
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ConfigurationError("BOT_TOKEN environment variable is not set")
    return token

async def start_bot():
    try:
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
        logger.error(f"Configuration error: {str(e)}")
        raise
    except TelegramAPIError as e:
        logger.error(f"Telegram API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
    except TelegramAPIError as e:
        logger.error(f"Telegram API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        logger.info("Bot stopped")
