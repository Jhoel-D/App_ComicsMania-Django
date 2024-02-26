# Generated by Django 5.0.2 on 2024-02-26 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0021_order_shipping_cost_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_method_cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
