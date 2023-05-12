import json

from django.core.management.base import BaseCommand

from catalog.models import Category, Book

class Command(BaseCommand):
    def handle(self, *args, **options):
        book_obj = Book.objects.all()
        for b in book_obj:
            converted_data_en = {
                "delta": "",
                "html": "EN " + b.content_uz.plain,
            }
            converted_data_ru = {
                "delta": "",
                "html": "RU " + b.content_uz.plain,
            }
            setattr(b, "content_en", json.dumps(converted_data_en))
            setattr(b, "content_ru", json.dumps(converted_data_ru))
            b.save(update_fields=["content_en", "content_ru"])

