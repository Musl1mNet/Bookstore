import django_filters

from catalog.models import Book, Author


class BookFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Book
        fields = ['authors', 'language', 'country', 'publisher']