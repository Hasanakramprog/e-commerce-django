# Generated by Django 5.0.4 on 2024-04-03 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_product_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
    ]