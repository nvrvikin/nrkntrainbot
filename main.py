from dotenv import load_dotenv
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher

from bot_handlers import text_handlers.router
from db_interactions import create_table

# Получение чувствительных данных (bot api) из среды
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

# логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Подключаем роутер сообщений в диспетчер
dp.include_router(text_handlers)

# Запуск процесса поллинга новых апдейтов
async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())