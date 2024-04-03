from typing import Dict, Any, Union
from src.models.models import User as UserModel
from telethon import events
from src.database.models import session, User


def get_user_by_telegram_id(user_id: str) -> User | None:
    user = session.query(User).filter(User.user_id == user_id).first()
    return user


def user_exists_or_create(event: events.NewMessage.Event) -> User:
    user = get_user_by_telegram_id(event.sender_id)
    if user:
        return user
    user = User(user_id=event.sender_id)
    session.add(user)
    session.commit()
    return user
