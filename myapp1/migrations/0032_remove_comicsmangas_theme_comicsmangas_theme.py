# Generated by Django 5.0.2 on 2024-09-18 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0031_remove_comicsmangas_category_comicsmangas_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comicsmangas',
            name='theme',
        ),
        migrations.AddField(
            model_name='comicsmangas',
            name='theme',
            field=models.ManyToManyField(to='myapp1.themes'),
        ),
    ]
