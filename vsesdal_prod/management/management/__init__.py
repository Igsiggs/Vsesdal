from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Запускаем Парсер"

    def handle(self, *args, **options):
        bot.polling(none_stop=True)
