from typing import Optional

from django.db import models
from django.shortcuts import redirect, resolve_url
from django.views.generic import TemplateView, ListView, DetailView
from django.utils.translation import gettext_lazy as _
from catalog.models import Book, Publisher, Category


class MainIndexView(TemplateView):
    template_name = "catalog/index.html"

    def get_field_randomly(self, field: Optional[list] = None, length: Optional[int] = 5):
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

        kwargs['publishers'] = self.get_field_randomly(publishers)  # get_field_randomly length default 5

        kwargs["ad_book4_6"] = ad_books[2:6]

        last_books = Book.objects.select_related('category').filter(status=Book.STATUS_PUBLISHED).order_by("-id")[:8]
        last_book_length = 8 if len(last_books) > 4 else 4
        kwargs["last_books"] = self.get_field_randomly(last_books, last_book_length)

        return kwargs


class MainList(ListView):
    template_name = "catalog/list.html"
    paginate_by = 24

    def get_queryset(self):
        cid = self.kwargs.get("id", None)
        query = Book.objects.order_by('-id')
        if cid is not None:
            cids = Category.objects.filter(path__contains=f"-{cid}-").only('id')
            query = query.filter(category_id__in=cids)

        return query

    def dispatch(self, request, *args, **kwargs):
        cid = kwargs.get("id", None)
        self.cat_objects = None
        if cid is not None:
            self.cat_objects = cat = Category.objects.get(id=cid)
            if kwargs.get("slug") != cat.slug:
                return redirect("catalog:list", cat.slug, cat.id, permanent=True)

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        bc = [{
            "url": resolve_url("catalog:books") if self.cat_objects else None,
            "title": _("Barcha kitoblar")
        }]
        if self.cat_objects:
            path = self.cat_objects.path.strip('-').split('-')
            path.pop()

            parents = list(Category.objects.filter(id__in=path).all())

            parents.sort(key=lambda r: path.index(str(r.id)))
            for row in parents:
                bc.append({
                    "url": resolve_url("catalog:list", row.slug, row.id),
                    "title": row.name
                })

            bc.append({
                "url": None,
                "title": self.cat_objects.name
            })
        children = Category.objects.filter(parent_id=None if self.cat_objects is None else self.cat_objects.id).order_by("-id").all()

        if not children:
            children = Category.objects.filter(parent_id=self.cat_objects.parent_id).order_by("-id").all()
        context['breadcrumb'] = bc
        context["children"] = children
        context['cid'] = None if self.cat_objects is None else self.cat_objects.id

        return context

class MainBookView(DetailView):
    model = Book
    template_name = "catalog/book.html"