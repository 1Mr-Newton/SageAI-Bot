import json
from telethon import events
from src.constants.system_message import system_message
from src.database.models import Conversation, User, session
from src.functions.get_convo_title import get_convo_title
from src.functions.safe_send import safe_send_message
import openai
from src.api.toolnames import tools
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam as UserMessage,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam as AssistantMessage,
)


async def process_response(
    event: events.NewMessage.Event,
    user: User,
    chat: ChatCompletion,
    messages: list[ChatCompletionMessageParam],
    response_message,
    user_current_conv,
) -> None:
    message = chat.choices[0].message
    is_tools_call = chat.choices[0].finish_reason == "tool_calls"

    if not is_tools_call:
        if message.content:
            assistant_message = AssistantMessage(
                content=message.content,
                role="assistant",
            )
            messages.append(assistant_message)

            await response_message.delete()
            await safe_send_message(event=event, message=message.content)
            user_current_conv.messages = json.dumps(messages)
            session.commit()
            title_message = [
                {
                    "role": "system",
                    "content": "You're a skilled namer. You look at a text and provide a short, memorable title for it. Your titles are about 20-60 characters long. You don't put your titles in quotes.",
                },
                {
                    "role": "user",
                    "content": f"""Provide a title for the following text:
                    {message.content}""",
                },
            ]
            title = get_convo_title(title_message)
            user_current_conv.title = title.replace('"', "")
            session.commit()

        else:
            await response_message.delete()
            await safe_send_message(
                event=event,
                message="Sorry, I could not understand your query. Please try again.",
            )
    else:
        await event.respond(
            "I need to use a tool to respond to your query. Please wait a moment..."
        )


async def process_ai_chat_message(event: events.NewMessage.Event, user: User) -> None:
    # Respond to the user indicating that the chatbot is processing their query
    response_message = await event.respond(
        "Please wait a moment while the chatbot responds to your query..."
    )

    # Retrieve the current conversation from the database

    user_current_conv = (
        session.query(Conversation)
        .filter(Conversation.id == user.current_conv_id)
        .first()
    )
    messages: list[ChatCompletionMessageParam] = (
        json.loads(str(user_current_conv.messages))
        if user_current_conv
        else [
            {
                "role": "system",
                "content": system_message,
            },
        ]
    )
    messages.append(
        UserMessage(
            content=event.raw_text,
            role="user",
        ),
    )

    # If there's no current conversation, create a new one and add it to the session
    if not user_current_conv:
        user_current_conv = Conversation(user_id=user.id, messages=json.dumps(messages))
        session.add(user_current_conv)
        session.commit()
        user.current_conv_id = user_current_conv.id
        session.commit()

    # messages = json.loads(str(user_current_conv.messages))

    # Generate a chat completion using OpenAI's API
    chat = openai.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        tools=tools,
        tool_choice="auto",
    )

    # Process the response from the chat completion
    await process_response(
        event=event,
        user=user,
        chat=chat,
        messages=messages,
        user_current_conv=user_current_conv,
        response_message=response_message,
    )
