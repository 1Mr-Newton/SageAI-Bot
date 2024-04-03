from src.tools.functions import generate_image, python_code_runner
from src.tools.gmail import send_mail


tools_dict = {
    "python_code_runner": python_code_runner,
    "send_mail": send_mail,
    "generate_image": generate_image,
}
