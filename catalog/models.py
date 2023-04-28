from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField
from django.core.validators import MinValueValidator
from catalog.decorators import i18n
from django.utils.decorators import method_decorator


class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nashriyot nomi")
    logo = models.ImageField(upload_to="publishers/")

    class Meta:
        verbose_name = "Nashriyot"
        verbose_name_plural = "Nashriyotlar"


class Author(models.Model):
    name = models.CharField(max_length=45, verbose_name="Muallif ismi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Muallif"
        verbose_name_plural = "Mualliflar"


@i18n
class Category(models.Model):
    parent = models.ForeignKey("Category", on_delete=models.RESTRICT, default=None, blank=True, null=True,
                               verbose_name="Otasi")
    name = models.CharField(max_length=45, blank=True, null=True, verbose_name="Nomi")

    path = models.CharField(max_length=50, default='-', db_index=True)

    @staticmethod
    def fix_path(pid, path):
        for row in Category.objects.filter(parent_id=pid).order_by('id').all():
            row.path = '-' + '-'.join(path + [str(row.id)]) + '-'
            row.save(fix=False)
            Category.fix_path(row.id, path + [str(row.id)])

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, fix=True
    ):
        ret = super().save(force_insert, force_update, using, update_fields)

        if fix:
            Category.fix_path(None, [])


    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.name)

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


@i18n
class Book(models.Model):
    STATUS_NEW = 0
    STATUS_PUBLISHED = 1
    STATUS_REJECTED = 2

    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    authors = models.ManyToManyField(Author)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    publisher = models.ForeignKey(Publisher, default=None, null=True, blank=True, on_delete=models.RESTRICT)

    name = models.CharField(max_length=250)

    content = models.TextField()

    photo = models.ImageField(upload_to="blocks/", default="default.jpg", blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[
        MinValueValidator(1000)
    ])
    status = models.IntegerField(choices=(
        (STATUS_NEW, "Yangi"),
        (STATUS_PUBLISHED, "Qabul qilingan"),
        (STATUS_REJECTED, "Inkor qilingan")
    ))
    rating_stars = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    availability = models.BooleanField(default=False)
    read = models.IntegerField(default=0)
    reading = models.IntegerField(default=0)
    will_read = models.IntegerField(default=0)
    publish_year = models.SmallIntegerField(default=None, blank=True, null=True)
    show_on_ad_block = models.BooleanField(default=False, db_index=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def short_info(self):
        return self.content[:100]

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return f"{self.name} ({self.id})"


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    language = models.CharField(max_length=10)
