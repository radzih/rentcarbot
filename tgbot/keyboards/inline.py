from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.services.db_api import get_car_types, get_cars_by_type

get_car_types_callback = CallbackData('get_car', 'type')
async def get_car_types_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    car_types = await get_car_types()
    for car_type in car_types:
        markup.add(
            InlineKeyboardButton(
                text=car_type,
                callback_data=get_car_types_callback.new(
                    type=car_type
                )
            )
        )
    markup.add(
        InlineKeyboardButton(
            text='❌Close',
            callback_data='close'
        )
    )
    return markup



navigation_car_callback = CallbackData('navi', 'index', 'type')
view_info_callback = CallbackData('car', 'car_id', 'index')
async def get_car_markup_and_photo_path(
    type: str,
    index: int=0) ->InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    cars = await get_cars_by_type(type)
    car_id = cars[index].id
    if len(cars) == 1:
        pass
    elif index == 0:
        markup.row(
            InlineKeyboardButton(
                text='⠀', 
                callback_data='first'
                ),
            InlineKeyboardButton(
                text='➡️', 
                callback_data=navigation_car_callback.new(
                    index=index+1,
                    type=type
                    )
                ),            
            )
    elif index == len(cars)-1:
        markup.row(
            InlineKeyboardButton(
                text='⬅️', 
                callback_data=navigation_car_callback.new(
                    index=index-1,
                    type=type
                    )
                ),            
            InlineKeyboardButton(
                text='⠀', 
                callback_data='last'
                ),
        )
    elif index != 0:
        markup.add(
            InlineKeyboardButton(
                text='⬅️', 
                callback_data=navigation_car_callback.new(
                    index=index-1,
                    type=type
                    )
                ),
            InlineKeyboardButton(
                text='➡️', 
                callback_data=navigation_car_callback.new(
                    index=index+1,
                    type=type
                    )
                ),
            )
    markup.add(
        InlineKeyboardButton(
            text='📄View info & Rent',
            callback_data=view_info_callback.new(
                car_id=car_id, 
                index=index
            )
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='↩️Back to brands',
            callback_data='show_brands'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='❌Close',
            callback_data='close'
        )
    )
    return markup, cars

rent_car_callback = CallbackData('rent','car_id')
show_photos_callback = CallbackData('show_photos', 'car_id')
photo_navigation_callback = CallbackData('photo_navigation', 'car_id', 'photo_index', 'index')
async def rent_car_markup(car_id: int, type: str, 
        navigation_index: int, photo_index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='⬅️ Previous photo',
                    callback_data=photo_navigation_callback.new(
                        car_id=car_id,
                        photo_index=photo_index-1,
                        index=navigation_index
                    )
                ),
                InlineKeyboardButton(
                    text='Next photo ➡️ ',
                    callback_data=photo_navigation_callback.new(
                        car_id=car_id,
                        photo_index=photo_index+1,
                        index=navigation_index
                    )
                ),
            ],
            [
                InlineKeyboardButton(
                    text='💸Rent',
                    callback_data=rent_car_callback.new(
                        car_id=car_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text='↩️Back to cars',
                    callback_data=navigation_car_callback.new(
                        index=navigation_index,
                        type=type,

                    )
                )
            ]
        ]
    )
    
cancel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='❌Cancel',
                callback_data='cancel'               
            )
        ]
    ]
)