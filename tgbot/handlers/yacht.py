from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from tgbot.keyboards.inline import cancel_markup

async def request_number_of_people(message: Message, state: FSMContext):
    await message.answer(
        text='How many people will be in a yacht',
        reply_markup=cancel_markup
        )
    await state.set_state('get_number_of_people')
    
async def get_number_of_people(message: Message, state: FSMContext):
    number_of_people = int(message.text)
    await message.answer(f'You have {number_of_people} people in a yacht')

async def say_that_is_not_number(message: Message, state: FSMContext):
    await message.answer(
        'It is not a number',
        reply_markup=cancel_markup)

async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer('canceled')
    await state.finish()
    

def register_yacht_handlers(dp: Dispatcher):
    dp.register_message_handler(
        request_number_of_people,
        commands=['yacht']
    )
    dp.register_message_handler(
        get_number_of_people,
        lambda m: m.text.isdigit(),
        state='get_number_of_people'
    )
    dp.register_callback_query_handler(
        cancel,
        state='get_number_of_people',
        text='cancel'
    )