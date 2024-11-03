import re

from typing import Any, List


SYMBOL_ALIASES = {
    "semantically entails": "\\Vdash",
    "not semantically entails": "\\nvdash",
    "syntactically entails": "\\vdash",
    "not syntactically entails": "\\nvdash",
    "subset": "\\subseteq",
    "not subset": "\\nsubseteq",
    "proper subset": "\\subset",
    "not proper subset": "\\nsubset",
    "union": "\\cup",
    "intersection": "\\cap",
    "set difference": "\\setminus",
    "empty set": "\\emptyset",
    "is in": "\\in",
    "is not in": "\\notin",
}

SYMBOL_TO_LATEX = [
    (r"⇒", r"$\\Rightarrow$"),
    (r"↦|↣|⟼", r"$\\mapsto$"),  # Removed extra "|" at the end
    (r"∈", r"$\\in$"),
    (r"⊆", r"$\\subseteq$"),
    (r"⊂", r"$\\subset$"),
    (r"∪", r"$\\cup$"),
    (r"∩", r"$\\cap$"),
    (r"∅", r"$\\emptyset$"),
    (r"∀", r"$\\forall$"),
    (r"∃", r"$\\exists$"),
    (r"∧", r"$\\land$"),
    (r"∨", r"$\\lor$"),
    (r"¬", r"$\\lnot$"),
    (r"→", r"$\\rightarrow$"),
    (r"↔|⟷", r"$\\leftrightarrow$"),
    (r"⊨", r"$\\Vdash$"),
    (r"⊭", r"$\\nvDash$"),
    (r"⊢", r"$\\vdash$"),
    (r"⊬", r"$\\nvdash$"),
    (r"⊣", r"$\\dashv$"),
    (r"⊤", r"$\\top$"),
    (r"⊥", r"$\\bot$"),
    (r"∞", r"$\\infty$"),
    (r"≠", r"$\\neq$"),
    (r"≤", r"$\\leq$"),
    (r"≥", r"$\\geq$"),
    (r"≈", r"$\\approx$"),
    (r"≡", r"$\\equiv$"),
]

def replace_symbols(input_str: str) -> str:
    # Apply each regex replacement in SYMBOL_TO_LATEX
    for pattern, replacement in SYMBOL_TO_LATEX:
        input_str = re.sub(pattern, replacement, input_str)
    return input_str

def symb_sub(input: str, subscript: str) -> str:
    return f"${SYMBOL_ALIASES.get(input, input)}_{{{subscript}}}$"

def symb(input: str) -> str:
    if input not in SYMBOL_ALIASES:
        msg = f"Symbol {input} not found in SYMBOL_ALIASES"
        raise KeyError(msg)

    return "$" + SYMBOL_ALIASES.get(input, input) + "$"


def t(input: str) -> str:
    return "$\\text{" + input + "}$"


def im(input: str) -> str:
    return "$" + input + "$"


def mm(input: str) -> str:
    return "$$" + input + "$$"


def st(input: List[Any]) -> str:
    return "$\\{" + ", ".join(map(str, input)) + "\\}$"
