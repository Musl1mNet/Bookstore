# Generated by Django 4.2.1 on 2023-05-08 19:33

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_alter_book_content_en_alter_book_content_ru_and_more'),
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
            name='name_en',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='book',
            name='name_ru',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=45, verbose_name='Nomi en'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=45, verbose_name='Nomi ru'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uz',
            field=models.CharField(max_length=45, verbose_name='Nomi uz'),
        ),
    ]
