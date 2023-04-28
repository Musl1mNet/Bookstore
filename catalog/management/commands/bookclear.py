import pathlib

from django.core.management.base import BaseCommand
from django.db import connection

from bookstore import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        with connection.cursor() as c:
            select = "SELECT photo FROM blocks WHERE status = 2;"
            delquery = "DELETE FROM blocks WHERE status = 2;"
            c.execute(select)
            photos = c.fetchall()
            for photo in photos:
                file = f"{photo[0]}"
                pathlib.Path(f"{settings.MEDIA_ROOT}" + str(file).replace("/img", "")).unlink()
            c.execute(delquery)
        print("Unpublish blocks clear success!")