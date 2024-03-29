# Generated by Django 4.2.1 on 2023-05-08 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_alter_category_name_en_alter_category_name_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='content_en',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='content_ru',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='content_uz',
            field=models.TextField(default=''),
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
            model_name='book',
            name='name_uz',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, default=None, max_length=45, null=True, verbose_name='Nomi en'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(blank=True, default=None, max_length=45, null=True, verbose_name='Nomi ru'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uz',
            field=models.CharField(blank=True, default=None, max_length=45, null=True, verbose_name='Nomi'),
        ),
    ]
