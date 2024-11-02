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
                # print(f"Terms for predicate {name}: {terms}")
                # predicate_under_interpretation = self.interpretation(name)(tuple(terms))
                # print(f"Predicate under interpretation: {predicate_under_interpretation}")
                # self.resolved_tokens = replace_range_in_list(
                #     self.resolved_tokens, start_pos, end_pos, predicate_under_interpretation
                # )
                # pretty_print_tokens(self.resolved_tokens)
            return Predicate(name, terms)
        raise ValueError(f"Expected predicate but got {token}")

    def term(self):
        token = self.peek()
        if token.type == "VARIABLE":
            return self.consume("VARIABLE").value
        elif token.type == "CONSTANT":
            return self.consume("CONSTANT").value
        raise ValueError(f"Unexpected term token: {token}")


def evaluate(node, interpretation: Interpretation):
    if isinstance(node, Predicate):
        # Base case: Evaluate the predicate with its terms
        return interpretation(node.name)(tuple(node.terms))

    elif isinstance(node, Not):
        # Negation: recursively evaluate and negate the result
        return not evaluate(node.expr, interpretation)

    elif isinstance(node, And):
        # Conjunction: both left and right must be true
        return evaluate(node.left, interpretation) and evaluate(
            node.right, interpretation
        )

    elif isinstance(node, Or):
        # Disjunction: either left or right (or both) must be true
        return evaluate(node.left, interpretation) or evaluate(
            node.right, interpretation
        )

    elif isinstance(node, Implies):
        # Implication: equivalent to ¬left ∨ right
        return not evaluate(node.left, interpretation) or evaluate(
            node.right, interpretation
        )

    elif isinstance(node, Quantifier):
        # Quantifiers: Handle both ∀ and ∃ quantifiers
        if node.quantifier == "∀":
            # Universal quantification: check for all objects in the domain
            for obj in interpretation.domain:
                # Temporarily bind the variable to the object
                interpretation.add_constant_object_mapping(Constant(node.variable), obj)
                if not evaluate(node.expr, interpretation):
                    interpretation.remove_constant_object_mapping(node.variable)
                    return False  # if any evaluation is False, ∀ fails
                interpretation.remove_constant_object_mapping(node.variable)
            return True  # all evaluations were True
        elif node.quantifier == "∃":
            # Existential quantification: check if any object in the domain satisfies
            for obj in interpretation.domain:
                interpretation.add_constant_object_mapping(Constant(node.variable), obj)
                if evaluate(node.expr, interpretation):
                    # Remove the temporary binding
                    interpretation.remove_constant_object_mapping(node.variable)
                    return True  # if any evaluation is True, ∃ succeeds
                interpretation.remove_constant_object_mapping(node.variable)
            return False  # none satisfied the expression
    else:
        raise ValueError(f"Unknown node type: {type(node)}")


def pretty_print_tokens(tokens):
    last_token = None
    for token in tokens:
        if isinstance(token, bool):
            if last_token != "NOT":
                print(" ", end="")
            print("TRUE " if token else "FALSE ", end="")
            last_token = "BOOL"
        elif isinstance(token, str):
            print(token, end="")
            last_token = token
        else:
            if token.value in SPACE_BEFORE:
                print(" ", end="")
            print(token.value, end="")
            if token.value in SPACE_AFTER:
                print(" ", end="")
            last_token = token.type
    print()


def replace_range_in_list(lst, start, end, replacement):
    buffer_n = end - start - 1
    return lst[:start] + [replacement] + [""] * buffer_n + lst[end:]
