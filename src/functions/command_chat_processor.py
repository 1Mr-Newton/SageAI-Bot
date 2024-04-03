from telethon import events
from src.commands.bot_commands import bot_commands_dict


async def command_chat_processor(event: events.NewMessage.Event):
    handler = bot_commands_dict[event.raw_text]
    await handler(event)
