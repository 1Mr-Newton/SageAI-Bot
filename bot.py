from src import *


@client.on(events.NewMessage())
async def new_message_handler(event: events.NewMessage.Event):

    await process_chat_message(event=event)


client.run_until_disconnected()
