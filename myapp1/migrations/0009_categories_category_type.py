# Generated by Django 5.0.2 on 2024-02-19 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0008_remove_categorytype_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='category_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp1.categorytype'),
            preserve_default=False,
        ),
    ]
