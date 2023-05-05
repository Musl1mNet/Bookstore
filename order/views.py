from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView

from catalog.models import Book
from order.froms import OrderForm
from order.models import Order, OrderBook


def cart_inc(request, id):
    cart_change(request, id, 1)
    print(id)
    return redirect(request.GET.get("to", "catalog:index"))


def cart_dec(request, id):
    cart_change(request, id, -1)
    return redirect(request.GET.get("to", "catalog:index"))


def cart_change(request, pid, n):
    p = Book.objects.get(id=pid)

    if p.status != Book.STATUS_PUBLISHED or p.available == 0:
        raise Http404()

    data = request.session.get("data", {})
    sid = str(p.id)
    if sid not in data:
        data[sid] = 0

    data[sid] += n
    data[sid] = min(p.available, data[sid])
    if data[sid] <= 0:
        del data[sid]

    request.session["data"] = data


class CheckoutView(CreateView):
    form_class = OrderForm
    template_name = "order/cart.html"

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return redirect("catalog:login")
        with transaction.atomic():
            data = self.request.session.get("data", {})
            books = []
            total_price = 0
            for k, v in data.items():
                book = Book.objects.select_for_update().get(id=k)
                if book.available < v or book.status != Book.STATUS_PUBLISHED:
                    return redirect("order:checkout")

                book.available -= v
                total_price += v * book.price
                book.save()

                books.append(
                    OrderBook(book_id=book.id, price=book.price, amount=v)
                )

            order = form.save(commit=False)
            order.user_id = self.request.user.id
            order.status = Order.STATUS_NEW
            order.payment_status = Order.PAYMENT_STATUS_NONE
            order.total_price = total_price
            order.save()

            for b in  books:
                b.order_id = order.id

            OrderBook.objects.bulk_create(books)

            del self.request.session["data"]

        return redirect("catalog:index")

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        data = self.request.session.get("data", {})
        book = Book.objects.filter(status=Book.STATUS_PUBLISHED, id__in=data.keys()).all()
        total_price = 0
        for row in book:
            row.in_cart = data.get(str(row.id), 0)
            row.total_price = row.in_cart * row.price
            total_price = row.total_price

        kwargs["books"] = book
        kwargs["total_price"] = total_price

        return kwargs