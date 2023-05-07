from typing import Optional

import MySQLdb
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView
from django.utils.translation import gettext_lazy as _

from catalog.filters import BookFilter
from catalog.forms import RegistrationForm, LoginForm
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
        query = Book.objects.only('id').all()
        if cid is not None:
            query = query.filter(category_id=cid)
        self.filter = f = BookFilter(self.request.GET, queryset=query[:1000])
        sql, params = f.qs.query.sql_with_params()
        sql = sql.replace("`catalog_book`.", '')
        print(sql, params)

        db = MySQLdb.connect(host="127.0.0.1", port=9306)
        cursor = db.cursor()
        cursor.execute(sql, params)

        rows = cursor.fetchall()

        book_ids = []
        for row in rows:
            book_ids.append(row[0])
        if book_ids:
            result = Book.objects.filter(id__in=book_ids).all()
        db.close()

        return result.order_by("-added_at")

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

        children = Category.objects.filter(
            parent_id=None if self.cat_objects is None else self.cat_objects.id).order_by("-id").all()

        if not children:
            children = Category.objects.filter(parent_id=self.cat_objects.parent_id).order_by("-id").all()
        context['breadcrumb'] = MainList.category_bc(self.cat_objects)
        context["children"] = children
        context['cid'] = None if self.cat_objects is None else self.cat_objects.id
        context['filter'] = self.filter

        return context

    @staticmethod
    def category_bc(object, last_active=False):
        bc = [{
            "url": resolve_url("catalog:books") if object else None,
            "title": _("Barcha kitoblar")
        }]
        if object:
            path = object.path.strip('-').split('-')
            path.pop()

            parents = list(Category.objects.filter(id__in=path).all())

            parents.sort(key=lambda r: path.index(str(r.id)))
            for row in parents:
                bc.append({
                    "url": resolve_url("catalog:list", row.slug, row.id),
                    "title": row.name
                })

            bc.append({
                "url": resolve_url("catalog:list", object.slug, object.id) if last_active else None,
                "title": object.name
            })

            return bc


class MainBookView(DetailView):
    model = Book
    template_name = "catalog/book.html"

    def get_queryset(self):
        if self.queryset:
            self.queryset.select_related("category").all()

        return Book.objects.select_related("category").all()

    def get_object(self, queryset=None):
        if not self.object:
            self.object = super().get_object(queryset=queryset)

        return self.object

    def dispatch(self, request, *args, **kwargs):
        self.object = None
        obj = self.get_object()
        if kwargs.get("slug") != obj.slug:
            return redirect("catalog:book", obj.slug, obj.id, permanent=True)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bc = MainList.category_bc(self.object.category, True)
        bc.append({
            "url": None,
            "title": self.object.name
        })
        context["breadcrumb"] = bc

        context["similar"] = Book.objects.filter(status=Book.STATUS_PUBLISHED).exclude(id=self.object.id).order_by(
            "?").all()[:4]

        return context

class MainSearchView(TemplateView):
    template_name = "catalog/search.html"

    def get_context_data(self, **kwargs):
        result = []
        q = self.request.GET.get('q', None)

        if q:
            db = MySQLdb.connect(host="127.0.0.1", port=9306)
            cursor = db.cursor()
            query = "SELECT id, weight() FROM catalog_book WHERE MATCH(%s) ORDER BY weight() ASC"
            cursor.execute(query, (q,))

            rows = cursor.fetchall()

            book_ids = []
            weights = {}
            for row in rows:
                weights[row[0]] = int(row[1])
                book_ids.append(row[0])
            if book_ids:
                result = list(Book.objects.filter(id__in = book_ids).all())
                result.sort(key=lambda r: weights[r.id])
            db.close()
        else:
            result = list(Book.objects.all())
        kwargs["result"] = result
        
        return super().get_context_data(**kwargs)









class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "user/registration.html"
    success_url = "catalog:login"

    def form_valid(self, form):

        user = form.save(commit=False)

        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect("catalog:login")
    def get_context_data(self, **kwargs):
        self.request.title = "Ro'yxatdan o'tish"
        return super().get_context_data(**kwargs)

class LoginView(FormView):
    form_class = LoginForm
    template_name = "user/login.html"
    success_url = "catalog:index"
    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect("catalog:index")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        self.request.title = "Tizimga kirish"
        return super().get_context_data(**kwargs)

@method_decorator(login_required, name='dispatch')
class UserInfoView(TemplateView):
    template_name = "user/myinfo.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

@login_required
def logout_view(request):
    logout(request)

    return redirect("catalog:index")
    
