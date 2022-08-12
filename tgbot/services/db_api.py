import os

import django
from asgiref.sync import sync_to_async

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin_panel.admin_panel.settings'
)
django.setup()

from admin_panel.database.models import Car, User, CarSerializer, \
    Company, CarType, MultiImagesCar


@sync_to_async
def get_car_types() -> list:
    objects = CarType.objects.all()
    return list(obj.name for obj in objects)

@sync_to_async
def get_cars_by_type(type: str) -> list:
    objects = Car.objects.filter(type__name=type)
    return list(objects)

@sync_to_async
def get_car_by_id(car_id: int) -> Car:
    car = Car.objects.get(id=car_id)
    return CarSerializer(car).data

@sync_to_async
def add_user(telegram_id: int, phone: str):
    User(
        telegram_id=telegram_id,
        phone=phone,
    ).save()

@sync_to_async
def get_user(telegram_id: int):
    return User.objects.get(telegram_id=telegram_id)

@sync_to_async
def get_users_telegram_ids() -> list:
    return list(
        User.objects.all().values('telegram_id')
    )

@sync_to_async
def get_company_channel_id(company: str) -> int:
    company = Company.objects.get(name=company)
    return company.channel_id

@sync_to_async
def get_car_images(car_id: int):
    return list(MultiImagesCar.objects.filter(car__id=car_id))