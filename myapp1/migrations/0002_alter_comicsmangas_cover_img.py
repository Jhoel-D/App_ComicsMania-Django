# Generated by Django 5.0.2 on 2024-10-13 20:31

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comicsmangas',
            name='cover_img',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Image'),
        ),
    ]
