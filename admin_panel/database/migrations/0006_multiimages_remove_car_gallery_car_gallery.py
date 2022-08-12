# Generated by Django 4.0.5 on 2022-06-27 12:22

import admin_panel.database.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_car_gallery_alter_car_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=admin_panel.database.models.car_photo_location_and_rename)),
            ],
        ),
        migrations.RemoveField(
            model_name='car',
            name='gallery',
        ),
        migrations.AddField(
            model_name='car',
            name='gallery',
            field=models.ManyToManyField(to='database.multiimages'),
        ),
    ]