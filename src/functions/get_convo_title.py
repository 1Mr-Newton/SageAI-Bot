import openai


def get_convo_title(messages: list) -> str:
    chat = openai.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    return chat.choices[0].message.content or "Conversation Title Not Found"
