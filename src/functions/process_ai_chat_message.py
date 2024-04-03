import json
import requests
from telethon import events
from src.api.api import get_chat_token
from uuid import uuid4
from src.constants.system_message import system_message
from src.constants.urls import openai_conversation_url
from src.functions.safe_send import safe_send_message
from src.models.models import User
import openai
from src.api.toolnames import tools
from openai.types.chat import ChatCompletion

#
import openai
import json
import os
from dotenv import load_dotenv
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam as UserMessage,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam as AssistantMessage,
)

from openai.types.chat.chat_completion_function_message_param import (
    ChatCompletionFunctionMessageParam as FunctionMessage,
)
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletion,
)
from constants.system_message import system_message
from time import perf_counter


async def process_response(
    event: events.NewMessage.Event,
    user: User,
    chat: ChatCompletion,
):
    message = chat.choices[0].message
    is_tools_call = chat.choices[0].finish_reason == "tool_calls"
    if not is_tools_call:
        assistant_message = AssistantMessage(
            content=message.content,
            role="assistant",
        )
        if message.content:
            # messages.append(assistant_message)
            await safe_send_message(event=event, message=message.content)
        else:
            await safe_send_message(
                event=event,
                message="Sorry I could not understand your query. Please try again.",
            )


async def process_ai_chat_message(event: events.NewMessage.Event, user: User) -> None:
    msg = await event.respond(
        "Please wait a moment while the chatbot responds to your query . . ."
    )

    chat = openai.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Don't make up information if you don't know the answer. Just say you don't know in a professional way.",
            },
            {
                "role": "user",
                "content": event.raw_text,
            },
        ],
        model="gpt-3.5-turbo",
        tools=tools,
        tool_choice="auto",
    )
    message = chat.choices[0].message
    is_tool_call = chat.choices[0].finish_reason == "tool_calls"

    print("is_tool_call", is_tool_call)

    await msg.edit("message")
