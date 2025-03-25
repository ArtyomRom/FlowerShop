import asyncio
import logging
from django.core.management.base import BaseCommand
from telegram_bot.bot import bot, dp  # Используем уже созданные объекты

logging.basicConfig(level=logging.INFO)

async def main():
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

class Command(BaseCommand):
    help = "Запускает Telegram-бота"

    def handle(self, *args, **kwargs):
        asyncio.run(main())  # Запускаем бота