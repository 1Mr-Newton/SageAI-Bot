import json
import requests
from telethon import events
from src.api.api import get_chat_token
from uuid import uuid4
from src.constants.system_message import system_message
from src.constants.urls import openai_conversation_url
from src.functions.safe_send import safe_send_message
from src.models.models import User


async def process_ai_chat_message(event: events.NewMessage.Event, user: User) -> None:

    oai_did = str(user.oai_id)
    token = get_chat_token(oai_did)
    headers = {
        "accept": "text/event-stream",
        "accept-language": "en-US,en;q=0.9,la;q=0.8,ru;q=0.7,es;q=0.6",
        "content-type": "application/json",
        "oai-device-id": oai_did,
        "oai-language": "en-US",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "openai-sentinel-chat-requirements-token": token,
    }

    body = {
        "action": "next",
        "messages": [
            {
                "id": str(uuid4()),
                "author": {"role": "system"},
                "content": {
                    "content_type": "text",
                    "parts": [system_message],
                },
                "metadata": {},
            },
            {
                "id": str(uuid4()),
                "author": {"role": "user"},
                "content": {
                    "content_type": "text",
                    "parts": [event.raw_text],
                },
                "metadata": {},
            },
        ],
        "parent_message_id": str(uuid4()),
        "model": "text-davinci-002-render-sha",
        "conversation_mode": {"kind": "primary_assistant"},
        "timezone_offset_min": 0,
        "suggestions": [],
        "history_and_training_disabled": False,
        "force_paragen": False,
        "force_paragen_model_slug": "",
        "force_rate_limit": False,
    }
    response = requests.post(
        openai_conversation_url,
        headers=headers,
        json=body,
        stream=True,
    )
    if response.status_code != 200:
        await event.respond(
            "An error occurred while processing your message. Please try again later."
        )
        return
    for line in response.iter_lines():
        if line:
            string_response = line.decode("utf-8")
            json_string = string_response.replace("data: ", "")
            try:
                data = json.loads(json_string)
                with open("data.json", "w") as f:
                    json.dump(data, f)
                message = data.get("message", {})
                isAssistant = message.get("author", {}).get("role") == "assistant"
                isFinished = message.get("status", {}) == "finished_successfully"
                if isAssistant and isFinished:
                    final_message = "\n".join(message.get("content", {}).get("parts"))
                    await safe_send_message(event, final_message)
                    return
            except json.JSONDecodeError:
                continue

    # await event.respond(f"Processing AI chat message: {message}")
