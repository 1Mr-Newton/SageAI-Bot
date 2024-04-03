from telethon import TelegramClient
from src.config.config import config

client = TelegramClient(
    "anon",
    config.API_ID,
    config.API_HASH,
).start(bot_token=config.BOT_TOKEN)
