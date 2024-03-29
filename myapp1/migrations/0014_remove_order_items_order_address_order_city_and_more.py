# Generated by Django 5.0.2 on 2024-02-25 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0013_remove_shoppingcartproduct_shopping_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='Otro', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='PayPal', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('PayPal', 'PayPal'), ('Mercado Libre', 'Mercado Libre'), ('Otro', 'Otro')], default='PayPal', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='zone',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
