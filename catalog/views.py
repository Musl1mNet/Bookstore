from django.shortcuts import render, resolve_url
from django.conf import settings
from django.db.models import F, Q, Case, When, Value, OuterRef, Subquery
from django.db.models import Count, Min, Max, Avg, Sum, FloatField
from django.db.models.functions import Length, Left, Coalesce
from datetime import datetime
from .models import Book, Author, Language, Category, Country
def show_books(request):
    savol = []
    books = {}
    txt = ""
    with open(f"{settings.BASE_DIR}/savollar.txt", "r") as s:
        savol = s.readlines()
    if request.POST:
        misol = ""
        if request.POST.get("misol"):
            misol = request.POST.get("misol")
            misol = int(misol)
        else:
            books = Book.objects.values("id", "name", "content").order_by("id")
        if misol == 1:
            books = Book.objects.values("id", "name", "added_at").order_by("-added_at")[:10]
        elif misol == 2:
            books = Book.objects.values("id", "name", "added_at").filter(added_at__year = datetime.now().year, read = 0)
        elif misol == 3:
            books = Book.objects.values("id", "name", "added_at", "read").filter(added_at__year = datetime.now().year - 1).order_by("-added_at")[:10]
        elif misol == 4:
            books = Book.objects.filter(status = Book.STATUS_PUBLISHED).aggregate(Count("status", output_field=FloatField()))
            txt = "Statusi qabul qilinga kitoblar soni: "
        elif misol == 5:
            books = Book.objects.values("id", "name", "publish_year", "category_id").filter(publish_year = 2005, category_id__in = [1, 2]).order_by("?")[:10]
        elif misol == 6:
            books = Book.objects.values("id", "name", "price", "read").order_by("price", "-read")[:10]
        elif misol == 7:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count")).values("id", "name", "added_at", "rating").filter(added_at__month = datetime.now().month - 1).order_by("-rating")[:10]
        elif misol == 8:
            books = Book.objects.values("id", "name", "added_at", "updated_at").filter(added_at = F("updated_at")).order_by("-added_at")[:10]
        elif misol == 9:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count"), name_len = Length("name")).values("id", "name", "rating").filter(name_len__lt = 5).order_by("rating")[:10]
        elif misol == 10:
            books = Book.objects.values("id", "name", "publish_year").filter(publish_year__in = [2010, 2015, 2020]).order_by("?")[:10]
        elif misol == 11:
            books = Book.objects.values("id", "name", "price", "publish_year").filter(publish_year__gt = datetime.now().year - 3).order_by("-price")
        elif misol == 12:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count")).values("id", "name", "price", "rating").order_by("-price", "rating")
        elif misol == 13:
            books = Book.objects.values("id", "name", "read", "will_read").filter(read__gt = F("will_read")).order_by("id")
        elif misol == 14:
            books = Book.objects.values("id", "name", "added_at", "updated_at").exclude(added_at = F("updated_at")).order_by("-id")[:10]
        elif misol == 15:
            books = Book.objects.values("id", "name", "content").filter(name__istartswith = "A").order_by("?")[:10]
        elif misol == 16:
            books = Book.objects.values("id", "name", "content", "category_id").filter(name__istartswith = "De", category_id__in = [1, 2, 3]).order_by("id")
        elif misol == 17:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count")).values("id", "name", "rating").filter(category_id__in = [1, 2]).order_by("-rating")
        elif misol == 18:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count")).values("id", "name", "country_id", "language_id", "rating").filter(country_id = 1).exclude(language_id = 1).order_by("-rating")
        elif misol == 19:
            books = Book.objects.values("id", "name", "country_id", "availability").filter(name__istartswith__in = ["A", "R", "S"]).exclude(country_id = 1, availability = True).order_by("id")
        elif misol == 20:
            books = Book.objects.values("id", "name", "read", "reading", "will_read").filter(read = F("reading"), reading = F("will_read")).exclude(read = 0)
        elif misol == 21:
            books = Book.objects.values("category__name").annotate(min_price = Min("price"))[:10]
        elif misol == 22:
            books = Book.objects.values("country__name", "language__name").annotate(books_count = Count("id"))
        elif misol == 23:
            books = Book.objects.values("publish_year").annotate(max_read = Max("read")).filter(publish_year__gt = datetime.now().year - 10)
        elif misol == 24:
            books = Book.objects.values(name_alfa = Left("name", 1)).annotate(max_rating = Max(F("rating_stars") / F("rating_count"))).order_by("-max_rating")
        elif misol == 25:
            books = Book.objects.values(name_alfa = Left("name", 1)).annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 26:
            books = Book.objects.values("status").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 27:
            books = Book.objects.values("added_at__year").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 28:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count"), rating_btw = Case(
                When(Q(rating__gt = 4) & Q(rating__lte = 5), then=Value("4-5")),
                When(Q(rating__gt = 3) & Q(rating__lte = 4), then=Value("3-4")),
                When(Q(rating__gt = 2) & Q(rating__lte = 3), then=Value("2-3")),
                When(Q(rating__gt = 1) & Q(rating__lte = 2), then=Value("1-2")),
                default=Value("0-1")
            )).values("rating_btw").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 29:
            books = Book.objects.values("added_at__month").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 30:
            books = Book.objects.values("status", "availability").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 31:
            books = Book.objects.annotate(price_status = Case(
                When(Q(price__gte = 1000000), then=Value("Qimmat")),
                When(Q(price__lte = 100000), then=Value("Arzon")),
                default=Value("O'rtacha")
            )).values("price_status").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 32:
            books = Book.objects.annotate(price_status = Case(
                When(Q(price__gte = 1000000), then=Value("Qimmat")),
                When(Q(price__lte = 100000), then=Value("Arzon")),
                default=Value("O'rtacha")
            )).values("country__name","price_status").annotate(books_count = Count("id")).order_by("country_id")
        elif misol == 33:
            books = Book.objects.annotate(price_status = Case(
                When(Q(price__gte = 1000000), then=Value("Qimmat")),
                When(Q(price__lte = 100000), then=Value("Arzon")),
                default=Value("O'rtacha")
            )).values("country__name", "language__name","price_status").annotate(books_count = Count("id")).order_by("country_id")
        elif misol == 34:
            books = Book.objects.annotate(price_status = Case(
                When(Q(price__gte = 1000000), then=Value("Qimmat")),
                When(Q(price__lte = 100000), then=Value("Arzon")),
                default=Value("O'rtacha")
            )).values("id", "name", "price", "price_status").order_by("price")
            books.filter(price_status = "Arzon").union(books.filter(price_status = "O'rtacha"), books.filter(price_status = "Qimmat"))
        elif misol == 35:
            books = Book.objects.annotate(rating = F("rating_stars") / F("rating_count"), 
            price_status = Case(
                When(Q(price__gte = 1000000), then=Value("Qimmat")),
                When(Q(price__lte = 100000), then=Value("Arzon")),
                default=Value("O'rtacha")
            ), 
            rating_btw = Case(
                When(Q(rating__gt = 4) & Q(rating__lte = 5), then=Value("4-5")),
                When(Q(rating__gt = 3) & Q(rating__lte = 4), then=Value("3-4")),
                When(Q(rating__gt = 2) & Q(rating__lte = 3), then=Value("2-3")),
                When(Q(rating__gt = 1) & Q(rating__lte = 2), then=Value("1-2")),
                default=Value("0-1")
            )).values("price_status", "rating_btw").annotate(books_count = Count("id")).order_by("price_status", "rating_btw")
        elif misol == 36:
            books = Book.objects.values("name").annotate(books_count = Count("id")).exclude(books_count = 1)
        elif misol == 37:
            books = Book.objects.values("language__name", "publish_year").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 38:
            books = Book.objects.values("category__name").annotate(books_count = Count("id")).filter(rating_count = 0).order_by("-books_count")
        elif misol == 39:
            books = Book.objects.values("category__name", "language__name").annotate(books_count = Count("id")).filter(rating_count = 0).order_by("-books_count")
        elif misol == 40:
            books = Book.objects.values("publish_year").annotate(books_count = Count("id")).order_by("-books_count")[:3]
        elif misol == 41:
            books = Book.objects.aggregate(avarage = Avg("price"))
            txt = "Jami kitoblarning o'rtacha narxi" 
        elif misol == 42:
            books = Book.objects.values("category__name").annotate(books_count = Count("id")).filter(category__name__istartswith = "f").order_by("-books_count")
        elif misol == 43:
            books = Book.objects.values("language__name").annotate(books_count = Count("id")).order_by("-books_count")
        elif misol == 44:
            books = Book.objects.prefetch_related("authors").values("authors__name").annotate(books_count = Count("id")).filter(authors__name__icontains = "a").order_by("-books_count")
        elif misol == 45:
            books = Book.objects.aggregate(rating_avarage = Avg(F("rating_stars") / F("rating_count")))
            txt = "Barcha kitoblarning o'rtacha reytingi: "
        elif misol == 46:
            books = Book.objects.values("category__name").annotate(max_rating = Max(F("rating_stars") / F("rating_count")), min_rating = Min(F("rating_stars") / F("rating_count")), rating_avarage = Avg(F("rating_stars") / F("rating_count"))).order_by("-category__name")
        elif misol == 47:
            books = Book.objects.values("language__name").annotate(read = Sum("read"), reading = Sum("reading"), will_read = Sum("will_read")).order_by("-language__name")
        elif misol == 48:
            books = Book.objects.values("authors__name").annotate(Younger = Max("publish_year"), Older = Min("publish_year")).order_by("authors__name")
        elif misol == 49:
            books = Book.objects.values("category__name").annotate(authors_c = Count("authors")).filter(authors_c = 2).order_by("authors__name")
        elif misol == 50:
            category = Category.objects.filter(id = OuterRef("category_id"), name__startswith = "F")
            books = Book.objects.annotate(cid = Subquery(category.values("id"))).filter(category_id = F("cid")).aggregate(Avg("price"))
            txt = "Y hari bilan boshlangan kategoriyalarga tegishli bo'lgan kitoblarning o'rtacha narxi: "
    else:
            books = Book.objects.values("id", "name", "content").order_by("id")
    return render(request, "table.html", context={
        "books" : books,
        "data": (books).values(),
        "txt" : txt
    })