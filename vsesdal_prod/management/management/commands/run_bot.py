from django.core.management.base import BaseCommand
from TgBot.main_bot import bot
import asyncio


class Command(BaseCommand):
    help = "Запускаем Бота"

    def handle(self, *args, **options):
        bot.polling(none_stop=True)
