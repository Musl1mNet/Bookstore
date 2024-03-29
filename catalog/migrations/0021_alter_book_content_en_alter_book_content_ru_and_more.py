# Generated by Django 4.2.1 on 2023-05-08 21:24

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_alter_book_content_en_alter_book_content_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='content_en',
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='content_ru',
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='content_uz',
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uz',
            field=models.CharField(blank=True, default=None, max_length=45, null=True, verbose_name='Nomi uz'),
        ),
    ]
