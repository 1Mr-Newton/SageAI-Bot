import json
from telethon import events, Button
from src.database.models import User, Conversation, session
from src.constants.system_message import system_message


async def start_handler(event: events.NewMessage.Event):
    await event.respond(
        "Hello! I'm a simple bot that can help you with your daily tasks. Type /help to see all available commands."
    )


async def help_handler(event: events.NewMessage.Event):
    await event.respond(
        "Here are the available commands:\n"
        "/start - Start the bot"
        "/help - Show this help message"
    )


async def about_handler(event: events.NewMessage.Event):
    await event.respond("This bot was created by me. I hope you find it useful!")


async def settings_handler(event: events.NewMessage.Event):
    await event.respond("Settings are not available yet.")


async def clear_handler(event: events.NewMessage.Event):
    await event.respond("Clearing chat history is not available yet.")


async def history_handler(event: events.NewMessage.Event):
    user = session.query(User).filter(User.user_id == event.sender_id).first()
    if not user:
        await event.respond(
            "You need to start the bot first. Type /start to start the bot."
        )
        return
    titles = [conv.title for conv in user.conversations if conv.title]

    await event.respond(
        "Here is your chat history\n\n",
        buttons=[
            [Button.inline(title, data=f"history_{title.replace(' ', '_')}")]
            for title in titles
        ],
    )


async def new_chat_handler(event: events.NewMessage.Event):

    user = session.query(User).filter(User.user_id == event.sender_id).first()
    if not user:
        await event.respond(
            "You need to start the bot first. Type /start to start the bot."
        )
        return
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
    ]
    conv = Conversation(user_id=user.id, messages=json.dumps(messages))
    session.add(conv)
    session.commit()
    user.current_conv_id = conv.id
    session.commit()

    await event.respond("New chat created. Send your message to start chatting.")
