from MySQLdb.constants.FIELD_TYPE import NULL
from django.db import models
from django.db.models import F
from django.utils.text import slugify
from django_quill.fields import QuillField
from django.core.validators import MinValueValidator
from catalog.decorators import i18n
from django.utils.decorators import method_decorator


class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nashriyot nomi")
    logo = models.ImageField(upload_to="publishers/")

    def __str__(self):
        return self.name

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
    name_uz = models.CharField(max_length=45, default=None, null=True, blank=True, verbose_name="Nomi uz")
    name_ru = models.CharField(max_length=45, default=None, null=True, blank=True, verbose_name="Nomi ru")
    name_en = models.CharField(max_length=45, default=None, null=True, blank=True, verbose_name="Nomi en")

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
        if fix:
            Category.fix_path(None, [])

        ret = super().save(force_insert, force_update, using, update_fields)
        return ret


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

    name_uz = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name_en = models.CharField(max_length=250)

    content_uz = QuillField()
    content_ru = QuillField()
    content_en = QuillField()

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
    available = models.IntegerField(default=0, validators=[
        MinValueValidator(0)
    ])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def short_info(self):
        return self.content.plain[:100]

    @property
    def slug(self):
        return slugify(self.name, allow_unicode=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

