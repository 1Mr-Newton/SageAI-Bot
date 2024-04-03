from telethon import events


async def start_handler(event: events.NewMessage.Event):
    await event.respond(
        "Hello! I'm a simple bot that can help you with your daily tasks. Type /help to see all available commands."
    )


async def help_handler(event: events.NewMessage.Event):
    await event.respond(
        "Here are the available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ping - Check if the bot is alive\n"
        "/echo <message> - Echo the message\n"
        "/add <num1> <num2> - Add two numbers\n"
        "/sub <num1> <num2> - Subtract two numbers\n"
        "/mul <num1> <num2> - Multiply two numbers\n"
        "/div <num1> <num2> - Divide two numbers\n"
    )


async def about_handler(event: events.NewMessage.Event):
    await event.respond("This bot was created by me. I hope you find it useful!")


# start_handler,
# help_handler,
# settings_handler,
# about_handler,
# clear_handler,
# history_handler,


async def settings_handler(event: events.NewMessage.Event):
    await event.respond("Settings are not available yet.")


async def clear_handler(event: events.NewMessage.Event):
    await event.respond("Clearing chat history is not available yet.")


async def history_handler(event: events.NewMessage.Event):
    await event.respond("Viewing chat history is not available yet.")
