from src.commands.bot_commands import bot_commands
from telethon import events
from src.database.helpers import user_exists_or_create
from src.functions.command_chat_processor import command_chat_processor
from src.functions.process_ai_chat_message import process_ai_chat_message
from src.config.client import client


async def process_chat_message(event: events.NewMessage.Event) -> None:
    user = user_exists_or_create(event=event)

    message_text = event.raw_text

    if message_text in bot_commands:
        await command_chat_processor(event)
        return

    await process_ai_chat_message(event, user=user)
