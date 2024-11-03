from collections import namedtuple
import re


Token = namedtuple("Token", ["type", "value"])

TOKEN_REGEX = [
    ("QUANTIFIER", r"[∀∃]"),
    ("VARIABLE", r"[a-z]"),
    ("PREDICATE", r"[A-Z]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("AND", r"∧"),
    ("OR", r"∨"),
    ("IMPLIES", r"→"),
    ("NOT", r"¬"),
    ("EQUAL", r"="),
    ("NEQUAL", r"≠"),
    ("COMMA", r","),
    ("WS", r"\s+"),  # Whitespace
    ("VARIABLE", r"\b[a-z]\b"),  # Single lowercase letter as a whole word
    ("PREDICATE", r"\b[A-Z]\b"),  # Single uppercase letter as a whole word
]

SYMBOL_REMAP = [
    (r"\bforall\b", "∀"),
    (r"\bexists\b", "∃"),
    (r"(\bimplies\b|=>|->|—>|→)", "→"),  # All implication symbols
    (r"(\band\b|&&|&)", "∧"),  # All AND symbols
    (r"(\bor\b|\|)", "∨"),  # All OR symbols
    (r"(\bnot\b|!)", "¬"),  # All NOT symbols
]

SYMBOL_REMAP_REGEX = [
    (re.compile(pattern), replacement) for pattern, replacement in SYMBOL_REMAP
]


def remap_symbols(formula: str) -> str:
    for pattern, replacement in SYMBOL_REMAP_REGEX:
        formula = pattern.sub(replacement, formula)
    return formula


def tokenize(formula: str, replace_aliases=True) -> list[Token]:
    if replace_aliases:
        formula = remap_symbols(formula)

    tokens = []
    pos = 0
    while pos < len(formula):
        match = None
        for token_type, regex in TOKEN_REGEX:
            regex = re.compile(regex)
            match = regex.match(formula, pos)
            if match:
                text = match.group(0)
                if token_type != "WS":
                    tokens.append(Token(token_type, text))
                pos = match.end(0)
                break
        if not match:
            raise ValueError(f"Unexpected character: {formula[pos]}")
    return tokens
