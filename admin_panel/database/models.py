import logging
from platform import mac_ver
import re
from uuid import uuid4
from attr import field
from django.db import models
from django.template import Engine
from rest_framework import serializers


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=20, unique=True)

def car_photo_location_and_rename(self, filename):
    if isinstance(self, MultiImagesCar):
        self = self.car
    file_extension = filename.split('.')[-1]
    brand = self.brand.name.replace(' ', '_')
    return f'data/car/images/{brand}/{uuid4()}.{file_extension}'

class CarBrand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Company(models.Model):
    name = models.CharField(max_length=100)
    channel_id = models.BigIntegerField(unique=True)
    
    def __str__(self):
        return self.name

class CarType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(CarType, on_delete=models.PROTECT)
    brand = models.ForeignKey(to=CarBrand, on_delete=models.PROTECT)
    one_to_three = models.DecimalField(decimal_places=0, max_digits=5)
    four_to_six = models.DecimalField(decimal_places=0, max_digits=5)
    seven_to_thirteen = models.DecimalField(decimal_places=0, max_digits=5)
    fourteen_to_twenty = models.DecimalField(decimal_places=0, max_digits=5)
    twenty_one_plus = models.DecimalField(decimal_places=0, max_digits=5)
    deposit = models.DecimalField(decimal_places=0, max_digits=5)
    daily_limit = models.IntegerField()
    year = models.CharField(max_length=100)
    colors = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.name
    
    def count_images(self):
        return MultiImagesCar.objects.filter(car=self).count()


class Yacht(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    feet = models.IntegerField()
    price_per_hour = models.DecimalField(decimal_places=0, max_digits=8)
    
    def __str__(self):
        return self.name

class MultiImagesCar(models.Model):
    car = models.ForeignKey(to=Car, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=car_photo_location_and_rename)

class MultiImagesYacht(models.Model):
    yacht = models.ForeignKey(to=Yacht, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=car_photo_location_and_rename)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id','name', 'channel_id')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id','name')

class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ('id', 'name')

class CarSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    brand = BrandSerializer()
    type = CarTypeSerializer()
    class Meta:
        model = Car
        fields = ('__all__')