import logging
from rich.logging import RichHandler
from utils.config import Config

most_recent_header = None
config = Config()

# Create a single file handler that all loggers will use
markdown_log_file = config.get_proj_root() / config["log_file"]["filename"]
shared_file_handler = logging.FileHandler(markdown_log_file, mode="w")

class MarkdownFormatter(logging.Formatter):
    """Custom formatter to output logs in Markdown format."""

    def format(self, record):
        # Skip debug level messages for Markdown file
        if record.levelno == logging.DEBUG:
            return ""

        # Header based on logger name
        level_header = f"# {record.name}"

        # Message formatted in Markdown with optional traceback info
        message = f"\n{record.getMessage()}\n"
        global most_recent_header
        if (
            level_header != most_recent_header
            and config["log_file"]["write_module_name_as_header"]
        ):
            message = f"\n{level_header}\n\n{message}"
            most_recent_header = level_header

        if record.exc_info:
            # Include traceback if there's an exception, wrapped as a Markdown code block
            message += f"\n```\n{self.formatException(record.exc_info)}\n```\n"

        return message


class Logger:
    def __init__(self, logger_name: str, level: int = logging.INFO):
        self.logger_base = logging.getLogger(logger_name)
        self.logger_base.setLevel(level)

        # Console handler with Rich formatting (unique to each logger)
        rich_handler = RichHandler(
            rich_tracebacks=True, tracebacks_show_locals=True, markup=True
        )
        console_formatter = logging.Formatter("%(message)s")
        rich_handler.setFormatter(console_formatter)
        self.logger_base.addHandler(rich_handler)

        # Shared file handler for Markdown logging
        markdown_formatter = MarkdownFormatter()
        shared_file_handler.setFormatter(markdown_formatter)

        # Attach the shared file handler if it's not already added
        if shared_file_handler not in self.logger_base.handlers:
            self.logger_base.addHandler(shared_file_handler)

    def __call__(self):
        return self.logger_base
