# Generated by Django 5.0.6 on 2024-06-21 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_decription_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brend',
        ),
    ]
