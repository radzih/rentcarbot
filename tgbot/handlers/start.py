from email import message
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import Dispatcher, FSMContext
from tgbot.filters.isregistered import IsRegistered
from tgbot.filters.notregistered import NotRegistered

from tgbot.keyboards.reply import get_phone_kb,remove_kb
from tgbot.services.db_api import add_user

async def start_bot(message: Message, state: FSMContext):
    await state.set_state('get_phone')
    await message.answer(
        text=(
            'Hi, i can help you to rent car\n'
            'but i need you phone, click button to share it'
        ),
        reply_markup=get_phone_kb,
    )

async def say_that_bot_started(message: Message):
    await message.answer(
        text='Bot already started'
    )

async def get_phone(message: Message, state: FSMContext):
    contact = message.contact.phone_number
    if message.contact.user_id == message.from_user.id:
        await state.finish()
        await message.answer(
            text='Thanks, you can rent car by typing /car',
            reply_markup=remove_kb
        )
        if '+' not in contact:
            contact = f'+{contact}'
        await add_user(message.from_user.id, contact)
    else:
        await message.answer(
            text='Its not your contact!!!'
        )

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_bot,
        CommandStart(),
        NotRegistered()
    )
    dp.register_message_handler(
        say_that_bot_started,
        CommandStart(),
        IsRegistered()
    )
    dp.register_message_handler(
        get_phone,
        content_types=ContentType.CONTACT,
        state='get_phone'
    )
