import logging

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery, MediaGroup
from aiogram.types.input_file import InputFile
from aiogram.types.input_media import InputMedia
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.isregistered import IsRegistered
from tgbot.keyboards.inline import get_car_types_markup,\
    get_car_types_callback, get_car_markup_and_photo_path,\
        navigation_car_callback, view_info_callback, rent_car_markup,\
            rent_car_callback, show_photos_callback, photo_navigation_callback
from tgbot.services.db_api import get_car_by_id, get_car_images, get_user


async def show_car_brands_message(message: Message):
    await message.answer_photo(
        photo=InputFile('./data/choose_brand.png'),
        caption='Choose car type',
        reply_markup=await get_car_types_markup()
    )

async def show_car_brands_call(call: CallbackQuery):
    await call.answer()
    await call.message.edit_media(
        media=InputMedia(
            media=InputFile('./data/choose_brand.png'),
            caption='Choose brand'
            ),
        reply_markup=await get_car_types_markup()
    )

async def show_cars(
    call: CallbackQuery, callback_data: dict):
    await call.answer()
    choosen_type = callback_data['type']
    index = int(callback_data.get('index', 0))
    markup, cars = await get_car_markup_and_photo_path(
        choosen_type,index=index) 
    car_object = cars[index]
    car_images = await get_car_images(car_object.id)
    media = InputMedia(
        media=InputFile(f'.{car_images[0].image.url}'),
        caption=(
            f'Car {index+1}/{len(cars)}\n'
            f'🏎{car_object.name}\n'
            f'<b>Price 1 to 3 day: {car_object.one_to_three} AED</b>\n'
            f'<b>Price 4 to 6 day: {car_object.four_to_six} AED</b>\n'
            f'<b>Price 7 to 13 day: {car_object.seven_to_thirteen} AED</b>\n'
            f'<b>Price 14 to 20 day: {car_object.fourteen_to_twenty} AED</b>\n'
            f'<b>Price 21+ day: {car_object.twenty_one_plus} AED</b>\n'
            )
        )
    await call.message.edit_media(
        media=media,
        reply_markup=markup,    
    )

async def show_info_about_car(call: CallbackQuery, callback_data: dict):
    await call.answer()
    car_id = int(callback_data['car_id'])
    navigation_index = int(callback_data['index'])
    car_images = await get_car_images(car_id)
    car_info = await get_car_by_id(car_id)
    photo_index = int(callback_data.get('photo_index', 0)) % len(car_images) 
    await call.message.edit_media(
        media=InputMedia(
            media=InputFile(f'.{car_images[photo_index].image.url}'),
            caption=(
                f'Photo {photo_index+1}/{len(car_images)}\n'
                f'🏎{car_info["name"]}\n'
                f'Brand: {car_info["brand"]["name"]}\n'
                f'Year: {car_info["year"]}\n'
                f'Colors: {car_info["colors"]}\n'
                f'Deposit: {car_info["deposit"]} AED\n'
                f'Daily limit: {car_info["daily_limit"]} km\n'
                f'<b>Price 1 to 3 day: {car_info["one_to_three"]} AED</b>\n'
                f'<b>Price 4 to 6 day: {car_info["four_to_six"]} AED</b>\n'
                f'<b>Price 7 to 13 day: {car_info["seven_to_thirteen"]} AED</b>\n'
                f'<b>Price 14 to 20 day: {car_info["fourteen_to_twenty"]} AED</b>\n'
                f'<b>Price 21+ day: {car_info["twenty_one_plus"]} AED</b>\n'
                '🔽<b>List photos</b>\n'
                ),
        ),
        reply_markup=await rent_car_markup(
            car_id, car_info['type']['name'], navigation_index, photo_index)
    )

async def send_rent_request(call: CallbackQuery, callback_data: dict):
    await call.answer()
    car_id = int(callback_data['car_id'])
    car_info = await get_car_by_id(car_id)
    user = await get_user(call.from_user.id)
    await call.bot.send_message(
        chat_id=car_info['company']['channel_id'],
        text=(
            'Hi, new customer\n'
            f'He want to rent {car_info["name"]}\n'
            f'His number {user.phone}'
        )
    )
    await call.message.edit_caption(
        caption='Request sended, wait for call'
    )

async def say_that_its_first_item(call: CallbackQuery):
    await call.answer('It\'s first item')

async def say_that_its_last_item(call: CallbackQuery):
    await call.answer('It\'s last item')

async def close_item(call: CallbackQuery):
    await call.answer('Closed')
    await call.message.delete()

def register_cars_handlers(dp: Dispatcher):
    dp.register_message_handler(
        show_car_brands_message,
        IsRegistered(),
        commands=['car'],
    )
    dp.register_callback_query_handler(
        show_car_brands_call,
        text='show_brands'
    )
    dp.register_callback_query_handler(
        show_cars,
        get_car_types_callback.filter(),
    )
    dp.register_callback_query_handler(
        show_cars,
        navigation_car_callback.filter(),
    )
    dp.register_callback_query_handler(
        show_info_about_car,
        view_info_callback.filter()
    )
    dp.register_callback_query_handler(
        send_rent_request,
        rent_car_callback.filter()
    )
    dp.register_callback_query_handler(
        show_info_about_car,
        photo_navigation_callback.filter()
    )
    dp.register_callback_query_handler(
        close_item, 
        text='close'
    )
    dp.register_callback_query_handler(
        say_that_its_first_item,
        text='first'
    )
    dp.register_callback_query_handler(
        say_that_its_last_item,
        text='last'
    )