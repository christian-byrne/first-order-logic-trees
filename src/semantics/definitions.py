import re

from utils.config import Config
from utils.log import Logger

from typing import Dict

config = Config()
logger = Logger(__name__, config["log_level"])()

definitions = None


def definition(term: str) -> str:
    global definitions
    if not definitions:
        parse_glossary()

    return definitions.get(term, None)


def define(term: str, definition: str):
    global definitions
    if not definitions:
        parse_glossary()

    if term in definitions:
        definition = definitions[term] + "\n\n" + definition

    definitions[term] = definition


def read_glossary_file() -> str:
    glossary_filepath = config.get_proj_root() / config["glossary_relative_path"]
    logger.debug(f"Reading glossary file from {glossary_filepath}")
    if not glossary_filepath.exists():
        msg = f"Glossary file not found at {glossary_filepath}"
        raise FileNotFoundError(msg)

    with open(glossary_filepath, "r") as file:
        return file.read()


def parse_glossary() -> Dict[str, str]:
    global definitions
    markdown_text = read_glossary_file()

    glossary_dict = {}
    lines = markdown_text.splitlines()

    logger.debug(f"Parsing glossary file with {len(lines)} lines")

    # Regex to match glossary term lines
    term_regex = r"^- \*\*(.+?)\*\*\s*$"
    term = None
    definition = []

    for line in lines:
        # Check if the line is a new term
        term_match = re.match(term_regex, line)

        if term_match:
            # If there was a previous term being built, save it to the glossary dictionary
            if term and definition:
                glossary_dict[term] = "\n".join(definition).strip()

            # Start a new term
            term = term_match.group(1)
            definition = []
        elif term:
            # Accumulate lines of the definition
            definition.append(line)

    # Add the last term
    if term and definition:
        glossary_dict[term] = "\n".join(definition).strip()

    logger.debug(f"Found {len(glossary_dict)} terms in the glossary")
    definitions = glossary_dict
    return glossary_dict
