from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

get_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='📞Share phone number',
                request_contact=True,
            )
        ]
    ],
    resize_keyboard=True
)

remove_kb = ReplyKeyboardRemove()