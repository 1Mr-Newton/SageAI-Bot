import os
from telethon import events
from telethon import TelegramClient, events, Button, functions, types
from telethon.tl.types import InputPeerUser, InputPeerChannel, InputPeerChat
from dotenv import load_dotenv
from src.config.client import client
from src.database.helpers import get_user_by_telegram_id
from src.models.models import User
from src.functions.chat_processor import process_chat_message
from src.functions.user_exit_or_create import user_exists_or_create
from src.functions.safe_send import safe_send_message
