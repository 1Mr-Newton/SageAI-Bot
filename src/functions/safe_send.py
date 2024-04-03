from telethon import events


async def safe_send_message(event: events.NewMessage.Event, message: str) -> None:
    """
    Sends a message to the user, splitting it into smaller messages if it exceeds Telegram's limit.
    """
    MAX_LENGTH = 4096  # Maximum length of a text message in Telegram

    if len(message) <= MAX_LENGTH:
        await event.respond(message)
    else:
        # If the message is too long, split it into parts and send each one separately
        for part in [
            message[i : i + MAX_LENGTH] for i in range(0, len(message), MAX_LENGTH)
        ]:
            await event.respond(part)
