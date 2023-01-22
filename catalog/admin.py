from django.contrib import admin
from django.utils.html import format_html

from catalog.forms import BookForm

from .models import Book, Language, Country, Author, Category

@admin.action(description="Status: NEW")
def book_status_new(modeladmin, request, queryset):
    queryset.update(status = Book.STATUS_NEW)

@admin.action(description="Status: PUBLISHED")
def book_status_publish(modeladmin, request, queryset):
    queryset.update(status=Book.STATUS_PUBLISHED)

@admin.action(description="Status: REJECTED")
def book_status_reject(modeladmin, request, queryset):
    queryset.update(status=Book.STATUS_REJECTED)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent', 'name']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ["name"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ["name"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookForm
    actions = [book_status_new, book_status_publish, book_status_reject]
    list_display = ['id', 'get_status_title','country', 'category', 'name', 'price', 'get_rating_stars', 'updated_at']
    list_filter = ['status', 'country', 'category', 'language']

    def get_status_title(self, obj):
        txt = obj.get_status_display()
        color = ""
        if obj.status == Book.STATUS_NEW:
            txt = "⏳ " + txt
            color = "#d35400"
        elif obj.status == Book.STATUS_PUBLISHED:
            txt = "✅ " + txt
        else:
            txt = "❌ " + txt
            color = "#c0392b"
        
        return format_html(f"""<span style = "color: {color}">{txt}</span> """)

    get_status_title.short_description = "Status"

    def get_rating_stars(self, obj):
        n = 0
        COLORY = "#feca57"
        COLORW = "#bdc3c7"
        if obj.rating_count > 0:
            n = round(obj.rating_stars / obj.rating_count)
        
        yellow_stars = f"""<span style = "color: {COLORY}">&#9733;</span> """ * n
        white_stars = f"""<span style = "color: {COLORW}">&#9733;</span> """ * (5 - n)
        return format_html(yellow_stars) + format_html(white_stars)

    get_rating_stars.short_description = "Reyting"


    autocomplete_fields = ["authors", "country"]