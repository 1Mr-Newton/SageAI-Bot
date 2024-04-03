from src import *
from pymongo import MongoClient


@client.on(events.NewMessage())
async def new_message_handler(event: events.NewMessage.Event):
    CONNECTION_STRING = "mongodb://root:tB8WhfnAi2Z3SjVQAjdv01r2eYnYz6WXJDNiPFMaX0MAZ3mexqBQs7l4yVNUsefy@w80cgkw:27017/?directConnection=true"

    client = MongoClient(CONNECTION_STRING)

    dbs = client.list_database_names()
    # await process_chat_message(event=event)
    print("Processing...")
    print(dbs)
    await event.respond("Hi")


client.run_until_disconnected()
