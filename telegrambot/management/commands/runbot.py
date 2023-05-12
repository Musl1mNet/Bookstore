from django.core.management.base import BaseCommand

from telegrambot.app import app


class Command(BaseCommand):

    def handle(self, *args, **options):

        app.run_polling()