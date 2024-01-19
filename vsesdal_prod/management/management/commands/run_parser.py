from django.core.management.base import BaseCommand
from Parser.main_parser import main

class Command(BaseCommand):
    help = "Запускаем Парсер"

    def handle(self, *args, **options):
        main()
