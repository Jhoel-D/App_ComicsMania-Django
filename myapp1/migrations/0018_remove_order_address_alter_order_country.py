# Generated by Django 5.0.2 on 2024-02-25 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0017_order_address_order_city_order_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(default='Bolivia', max_length=100),
        ),
    ]
