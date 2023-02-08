from django.shortcuts import render, resolve_url
from django.conf import settings
from django.db.models import F, Q
# from django.db.models.functions
from .models import Book, Language, Author, Country, Category
def show_books(request):
    savol = []
    with open(f"{settings.BASE_DIR}/savollar.txt", "r") as s:
        savol = s.readlines()
    if request.POST:
        misol = ""
        if request.POST.get("misol"):
            misol = request.POST.get("misol")
            # print(misol)
            misol = int(misol)
        else:
            books = Book.objects.values("id", "name", "content").order_by("id")
