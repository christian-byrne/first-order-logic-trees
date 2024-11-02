from collections import namedtuple
import re
from interpretation import Interpretation, Constant

from typing import List

# Define a Token named tuple for easier readability
Token = namedtuple("Token", ["type", "value"])

# Define token types with regex patterns
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
]

SPACE_BEFORE = []
SPACE_AFTER = ["→", "∧", "∨", "≠", "=", ","]


def tokenize(formula):
    tokens = []
    pos = 0
    while pos < len(formula):
        match = None
        for token_type, regex in TOKEN_REGEX:
            regex = re.compile(regex)
            match = regex.match(formula, pos)
            if match:
                text = match.group(0)
                if token_type != "WS":  # Ignore whitespace
                    tokens.append(Token(token_type, text))
                pos = match.end(0)
                break
        if not match:
            raise ValueError(f"Unexpected character: {formula[pos]}")
    return tokens


class Expr:
    pass


class Quantifier(Expr):
    def __init__(self, quantifier, variable, expr):
        self.quantifier = quantifier
        self.variable = variable
        self.expr = expr

    def __str__(self):
        return f"{self.quantifier}{self.variable}({self.expr})"


class Predicate(Expr):
    def __init__(self, name, terms=None):
        self.name = name
        self.terms = terms or []

    def __str__(self):
        term_str = ", ".join(map(str, self.terms))
        return f"{self.name}({term_str})"


class Not(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"¬{self.expr}"


class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∧ {self.right})"


class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∨ {self.right})"


class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} → {self.right})"


class Parser:
    def __init__(self, tokens: List[str], interpretation: Interpretation):
        self.tokens = tokens
        self.resolved_tokens = tokens[:]
        self.pos = 0
        self.current_evaluation = True
        self.interpretation = interpretation

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, token_type):
        token = self.peek()
        if token and token.type == token_type:
            self.pos += 1
            return token
        raise ValueError(f"Expected token {token_type} but got {token}")

    def parse(self):
        return self.expr()

    def expr(self):
        left = self.disjunct()
        token = self.peek()
        if token and token.type == "IMPLIES":
            self.consume("IMPLIES")
            right = self.disjunct()
            return Implies(left, right)
        return left

    def disjunct(self):
        left = self.conjunct()
        while self.peek() and self.peek().type == "OR":
            self.consume("OR")
            right = self.conjunct()
            left = Or(left, right)
        return left

    def conjunct(self):
        left = self.quantified()
        while self.peek() and self.peek().type == "AND":
            self.consume("AND")
            right = self.quantified()
            left = And(left, right)
        return left

    def quantified(self):
        if self.peek() and self.peek().type == "QUANTIFIER":
            quantifier = self.consume("QUANTIFIER").value
            variable = self.consume("VARIABLE").value
            expr = self.quantified()
            return Quantifier(quantifier, variable, expr)
        return self.negation()

    def negation(self):
        if self.peek() and self.peek().type == "NOT":
            self.consume("NOT")
            expr = self.negation()
            return Not(expr)
        elif self.peek() and self.peek().type == "LPAREN":
            # Parse a grouped expression in parentheses
            self.consume("LPAREN")
            expr = self.expr()  # Parse the inner expression
            self.consume("RPAREN")  # Expect a closing parenthesis
            return expr
        return self.predicate()

    def predicate(self):
        token = self.peek()
        if token.type == "PREDICATE":
            name = self.consume("PREDICATE").value
            terms = []
            if self.peek() and self.peek().type == "LPAREN":
                self.consume("LPAREN")
                terms.append(self.term())
                while self.peek() and self.peek().type == "COMMA":
                    self.consume("COMMA")
                    terms.append(self.term())
                self.consume("RPAREN")
            return Predicate(name, terms)
        raise ValueError(f"Expected predicate but got {token}")

    def term(self):
        token = self.peek()
        if token.type == "VARIABLE":
            return self.consume("VARIABLE").value
        elif token.type == "CONSTANT":
            return self.consume("CONSTANT").value
        raise ValueError(f"Unexpected term token: {token}")

