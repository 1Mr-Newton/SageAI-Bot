from src.models.models import User
from src.database.helpers import create_user, get_user_by_telegram_id
from telethon import events


def user_exists_or_create(event: events.NewMessage.Event) -> User | str:
    user = get_user_by_telegram_id(event.sender_id)

    return user if user else create_user(event)
