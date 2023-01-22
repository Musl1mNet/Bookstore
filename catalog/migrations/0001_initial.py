# Generated by Django 4.1.3 on 2023-01-09 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.category')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('photo', models.ImageField(upload_to='books/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.IntegerField(choices=[(0, 'Yangi'), (1, 'Qabul qilingan'), (2, 'Inkor qilingan')])),
                ('rating_stars', models.IntegerField(default=0)),
                ('rating_count', models.IntegerField(default=0)),
                ('avialability', models.BooleanField(default=False)),
                ('read', models.IntegerField(default=0)),
                ('reading', models.IntegerField(default=0)),
                ('will_read', models.IntegerField(default=0)),
                ('publish_year', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('authors', models.ManyToManyField(to='catalog.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalog.category')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalog.country')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalog.language')),
            ],
        ),
    ]
