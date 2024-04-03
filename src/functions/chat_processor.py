from src.commands.bot_commands import bot_commands
from telethon import events
from src.functions.command_chat_processor import command_chat_processor
from src.functions.process_ai_chat_message import process_ai_chat_message
from src.functions.user_exit_or_create import user_exists_or_create
from src.config.client import client


async def process_chat_message(event: events.NewMessage.Event) -> None:
    user_or_error = user_exists_or_create(event=event)

    if isinstance(user_or_error, str):
        await event.respond(user_or_error)
        return

    message_text = event.raw_text

    if message_text in bot_commands:
        await command_chat_processor(event)
        return

    await process_ai_chat_message(event, user=user_or_error)
