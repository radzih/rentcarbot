# Generated by Django 4.0.5 on 2022-06-27 12:49

import admin_panel.database.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_remove_car_gallery_multiimages_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='photo',
            field=models.ImageField(blank=True, upload_to=admin_panel.database.models.car_photo_location_and_rename),
        ),
    ]
