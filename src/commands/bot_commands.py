from src.commands.command_proccessors import (
    start_handler,
    help_handler,
    settings_handler,
    about_handler,
    clear_handler,
    history_handler,
)

bot_commands = ["/help", "/start", "/settings", "/about", "/clear", "/history"]


bot_commands_dict = {
    "/help": help_handler,
    "/start": start_handler,
    "/settings": settings_handler,
    "/about": about_handler,
    "/clear": clear_handler,
    "/history": history_handler,
}
