from typing import Optional

from django.db import models
from django.views.generic import TemplateView

from catalog.models import Book, Publisher



class MainIndexView(TemplateView):
    template_name = "catalog/index.html"

    def get_field_randomly(self, field:Optional[list]=None, length:Optional[int]=5):
        if field:
            idx = 0
            while len(field) < length:
                field.append(field[idx])
                idx += 1
        return field

    def get_context_data(self, **kwargs):
        ad_books = list(Book.objects.filter(status=Book.STATUS_PUBLISHED, show_on_ad_block=True).order_by("?")[:7])

        if not ad_books:
            ad_books = list(Book.objects.filter(status=Book.STATUS_PUBLISHED).order_by("?")[:7])

        kwargs['ad_books'] = self.get_field_randomly(ad_books, length=7)

        publishers = list(Publisher.objects.order_by("?")[:5])

        kwargs['publishers'] = self.get_field_randomly(publishers) # get_field_randomly length default 5

        kwargs["ad_book4_6"] = ad_books[2:6]

        last_books = Book.objects.select_related('category').filter(status=Book.STATUS_PUBLISHED).order_by("-id")[:8]
        last_book_length = 8 if len(last_books) > 4 else 4
        kwargs["last_books"] = self.get_field_randomly(last_books, last_book_length)

        return kwargs


