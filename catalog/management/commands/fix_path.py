from django.core.management.base import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.fix_path(None, [])