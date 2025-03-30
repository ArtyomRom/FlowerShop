import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from telegram_bot.bot_tools import handlers
# Загружаем переменные окружения
load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Импортируем и регистрируем обработчики (если они есть)
from telegram_bot.bot_tools import handlers

dp.include_router(handlers.router)  # Приветственное сообщение
# dp.include_router(orders.router)  # Заказы