# Generated by Django 5.0.6 on 2024-06-27 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('shop.product',),
        ),
    ]