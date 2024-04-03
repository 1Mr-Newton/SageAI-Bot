from src.database.connector import supabaseClient
from typing import Dict, Any, Union
from src.models.models import User
from src.api.api import get_oai_did
from telethon import events


def get_user_by_telegram_id(user_id: str) -> User | None:
    data = supabaseClient.from_("user").select("*").eq("user_id", user_id).execute()
    response_data: list[Dict[str, Any]] = data.data
    if len(response_data) > 0:
        return User(**response_data[0])
    return None


def create_user(event: events.NewMessage.Event) -> User | str:

    oai_did = get_oai_did()
    if oai_did is None:
        return "Unable to create your account. Please try again later."

    try:
        data = (
            supabaseClient.from_("user")
            .insert(
                {
                    "user_id": event.sender_id,
                    "oai_id": oai_did,
                    "display_name": event.sender.first_name,
                }
            )
            .execute()
        )

        response_data: Dict[str, Any] = data.data[0]
        return User(**response_data)
    except Exception as e:
        # Log the exception e here if you have logging set up
        print(e)
        return "An unexpected error occurred. Please try again later."
