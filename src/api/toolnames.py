from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition
from openai.types.shared_params.function_parameters import FunctionParameters
from openai.types.chat.completion_create_params import Function

python_code_runner_tool = ChatCompletionToolParam(
    function=FunctionDefinition(
        description="Runs arbitrary Python code",
        name="python_code_runner",
        parameters={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute",
                }
            },
            "required": ["code"],
        },
    ),
    type="function",
)

send_mail_tool = ChatCompletionToolParam(
    function=FunctionDefinition(
        description="Send an email",
        name="send_mail",
        parameters={
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "The email address to send the email to",
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email",
                },
                "body": {
                    "type": "string",
                    "description": "The body of the email",
                },
                "attachments": {
                    "type": "array",
                    "description": "A list of file paths or URLs to attach to the email",
                    "items": {"type": "string"},
                },
            },
            "required": ["to", "subject", "body"],
        },
    ),
    type="function",
)


generate_image_tool = ChatCompletionToolParam(
    function=FunctionDefinition(
        description="Generate an image based on a prompt.",
        name="generate_image",
        parameters={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt to generate the image from",
                }
            },
            "required": ["prompt"],
        },
    ),
    type="function",
)


tools = [python_code_runner_tool, send_mail_tool, generate_image_tool]
