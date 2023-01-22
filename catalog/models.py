from django.db import models
from django_quill.fields import QuillField


class Author(models.Model):
    name = models.CharField(max_length=45, verbose_name="Muallif ismi")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Muallif"
        verbose_name_plural = "Mualliflar"

class Category(models.Model):
    parent = models.ForeignKey("Category", on_delete=models.RESTRICT, default=None, blank=True, null=True, verbose_name="Otasi")
    name = models.CharField(max_length=45, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nomi")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Til"
        verbose_name_plural = "Tillar"

class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nomi")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Davlat"
        verbose_name_plural = "Davlatlar"

class Book(models.Model):
    STATUS_NEW = 0
    STATUS_PUBLISHED = 1
    STATUS_REJECTED = 2

    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    authors = models.ManyToManyField(Author)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    name = models.CharField(max_length=250)
    content = models.TextField()
    photo = models.ImageField(upload_to="books/")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=(
        (STATUS_NEW, "Yangi"),
        (STATUS_PUBLISHED, "Qabul qilingan"),
        (STATUS_REJECTED, "Inkor qilingan")
    ))
    rating_stars = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    avialability = models.BooleanField(default=False)
    read = models.IntegerField(default=0)
    reading = models.IntegerField(default=0)
    will_read = models.IntegerField(default=0)
    publish_year = models.SmallIntegerField(default=None, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.id})"