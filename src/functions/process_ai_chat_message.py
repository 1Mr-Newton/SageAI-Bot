import json
from telethon import events
from src.constants.system_message import system_message
from src.database.models import Conversation, User, session
from src.functions.get_convo_title import get_convo_title
from src.functions.safe_send import safe_send_message
import openai
from src.api.toolnames import tools
from src.api.tools_dict import tools_dict
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam as UserMessage,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam as AssistantMessage,
)
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam as ToolMessage,
)
from src.config.client import client


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
            if not user_current_conv.title:
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
        tools_calls = message.tool_calls

        if tools_calls:
            tool = tools_calls[0]
            toolName = tool.function.name

            args: dict = json.loads(str(tool.function.arguments))

            func_to_call = tools_dict[toolName]
            response = func_to_call(**args)

            tool_message = ToolMessage(
                content=response,
                role="tool",
                tool_call_id=tool.id,
            )
            assistant_message = AssistantMessage(
                content=message.content,
                role="assistant",
                tool_calls=[json.loads(tc.model_dump_json()) for tc in tools_calls],
                name=toolName,
            )
            messages.append(assistant_message)

            messages.append(tool_message)
            if (
                toolName == "generate_image"
                and response
                != "An error occurred while generating the image. Please try again later."
            ):
                await client.send_file(event.sender_id, response)

            chat = openai.chat.completions.create(
                messages=messages,
                model="gpt-3.5-turbo",
                tools=tools,
                tool_choice="auto",
            )
            return await process_response(
                chat=chat,
                event=event,
                user=user,
                messages=messages,
                response_message=response_message,
                user_current_conv=user_current_conv,
            )

        await event.respond(
            "Sorry, I could not understand your query. Please try again."
        )


async def process_ai_chat_message(event: events.NewMessage.Event, user: User) -> None:
    response_message = await event.respond("Please wait a moment...")

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
