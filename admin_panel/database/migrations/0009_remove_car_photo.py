# Generated by Django 4.0.5 on 2022-06-30 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_alter_car_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='photo',
        ),
    ]
