import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
import g4f

# Укажите токен вашего Telegram-бота
BOT_TOKEN = "7952594519:AAGt2FyMf2oHACUNFbLkH-dgeXd1JF3UOFU"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Установка параметров по умолчанию для бота
default_properties = DefaultBotProperties(parse_mode="HTML")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=default_properties)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    logger.info(f"Received /start command from {message.from_user.id}")
    await message.answer("Привет! Напиши мне сообщение, и я отвечу с помощью GPT-4.")

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    user_input = message.text
    logger.info(f"Received message from {message.from_user.id}: {user_input}")

    try:
        # Отправка запроса в GPT-4 через g4f
        logger.info("Sending request to GPT-4 via g4f...")
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )

        # Логирование полного ответа от g4f
        logger.info(f"Full response from g4f: {response}")

        # Проверка на успешный ответ
        if isinstance(response, str):
            # Если ответ является строкой
            bot_reply = response
            logger.info(f"Reply from GPT-4: {bot_reply}")
            await message.answer(bot_reply)
        else:
            logger.error("No valid response from GPT-4.")
            await message.answer("Произошла ошибка при получении ответа от GPT-4.")

    except Exception as e:
        logger.error(f"Error while processing message: {e}")
        await message.answer(f"Ошибка при обработке запроса: {e}")

# Запуск бота
async def main():
    logger.info("Bot started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
