# # from telegram import Update
# # from telegram.ext import Updater, CommandHandler, CallbackContext
# import os
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import Application, CommandHandler
# load_dotenv()
#
# # Твой API Token
# TELEGRAM_TOKEN = os.environ.get('TOKEN_BOT')
#
# # Функция для команды /start
# async def start(update: Update, context):
#     await update.message.reply_text('Привет! Я твой цветочный бот!')
#
# # Главная функция
# def main():
#     # Создаем приложение (не Updater)
#     application = Application.builder().token(TELEGRAM_TOKEN).build()
#
#     # Регистрируем команду /start
#     application.add_handler(CommandHandler("start", start))
#
#     # Запускаем бота
#     application.run_polling()
#
# if __name__ == '__main__':
#     main()

# import asyncio
# import logging
# import os
# from aiogram import Bot, Dispatcher
# from django.core.management.base import BaseCommand
# from dotenv import load_dotenv  # Читаем переменные из .env
#
# # Загружаем переменные окружения
# load_dotenv()
#
# TOKEN = os.getenv("TOKEN_BOT")
#
# if not TOKEN:
#     raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")
#
# # Включаем логирование
# logging.basicConfig(level=logging.INFO)
#
# async def main():
#     bot = Bot(token=TOKEN)
#     dp = Dispatcher()
#
#     # Регистрируем обработчики (если у тебя есть файлы с хэндлерами)
#     # from telegram_bot.staticfiles import router
#     # dp.include_router(router)
#
#     logging.info("Бот запущен!")
#     await dp.start_polling(bot)

# class Command(BaseCommand):
#     help = "Запускает Telegram-бота"
#
#     def handle(self, *args, **kwargs):
#         asyncio.run(main())
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Импортируем и регистрируем обработчики (если они есть)
from telegram_bot.staticfiles import handlers

dp.include_router(handlers.router)  # Приветственное сообщение
# dp.include_router(orders.router)  # Заказы