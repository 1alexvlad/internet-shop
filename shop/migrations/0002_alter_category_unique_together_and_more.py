# Generated by Django 5.0.6 on 2024-06-19 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
    ]
