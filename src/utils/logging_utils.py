import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.emoji import Emoji

console = Console()

def setup_logging():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )

def log_info(message, emoji_name=None):
    emoji = f"{Emoji(emoji_name)} " if emoji_name else ""
    console.log(f"{emoji}{message}", style="bold blue")

def log_error(message, emoji_name=None):
    emoji = f"{Emoji(emoji_name)} " if emoji_name else ""
    console.log(f"{emoji}{message}", style="bold red")

def log_success(message, emoji_name=None):
    emoji = f"{Emoji(emoji_name)} " if emoji_name else ""
    console.log(f"{emoji}{message}", style="bold green")

def log_warning(message, emoji_name=None):
    emoji = f"{Emoji(emoji_name)} " if emoji_name else ""
    console.log(f"{emoji}{message}", style="bold yellow")