# Generated by Django 5.0.2 on 2024-02-16 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0004_categories_genres_languages_paymentmethods_publisher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
