# Generated by Django 5.0.6 on 2024-07-22 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='products/products/default/image.png', upload_to='products/products/%Y/%m/%d', verbose_name='Изображение'),
        ),
    ]
