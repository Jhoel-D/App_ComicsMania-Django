# Generated by Django 5.0.2 on 2024-02-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0028_remove_cartitem_included_in_order_itemsorder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='orders', to='myapp1.itemsorder'),
        ),
    ]
