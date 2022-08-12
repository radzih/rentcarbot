import logging
from aiogram.dispatcher.filters import BoundFilter

from tgbot.services.db_api import get_users_telegram_ids


class IsRegistered(BoundFilter):
    async def check(self, obj):
        return obj.from_user.id in [
            int(user.get('telegram_id')) for user in await get_users_telegram_ids() 
            ]

