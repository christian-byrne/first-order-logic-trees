from utils.config import Config

config = Config()

def h(title: str, level: int) -> str:
    return "#" * level + " " + title + "\n\n"


def df(term_name: str, definition) -> str:
    # Capitalize term name
    term_name = term_name.capitalize()

    # Create multiline quote block
    definition = definition.replace("\n", "\n> ")

    return f"\n> **{term_name}**: {definition}\n\n"

def pic(filename: str, alt_text: str = "alt text") -> str:
    path = config.get_proj_root() / config["output_relpath"] / filename
    return f"\n![{alt_text}]({path})\n\n"