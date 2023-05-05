from django.contrib.auth.models import User
from django.db import models

from catalog.models import Book


class Order(models.Model):
    STATUS_NEW = 0
    STATUS_ACCEPTED = 1
    STATUS_REJECTED = 2

    PAYMENT_STATUS_NONE = 0
    PAYMENT_STATUS_PREPARE = 1
    PAYMENT_STATUS_PAID = 2
    PAYMENT_STATUS_CACELED = 3

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    address = models.TextField()
    zip = models.CharField(max_length=10)
    total_price = models.IntegerField()
    status = models.SmallIntegerField(choices=
                                      (
                                          (STATUS_NEW, "Yangi"),
                                          (STATUS_ACCEPTED, "Qabul qilingan"),
                                          (STATUS_REJECTED, "Inkor qilingan")
                                      ))
    payment_status = models.SmallIntegerField(choices=
                                      (
                                          (PAYMENT_STATUS_NONE, "Noaniq"),
                                          (PAYMENT_STATUS_PREPARE, "Jarayonda"),
                                          (PAYMENT_STATUS_PAID, "To'langan"),
                                          (PAYMENT_STATUS_CACELED, "Bekor qilingan")
                                      ))
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderBook(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    price = models.IntegerField()
    amount = models.IntegerField()
