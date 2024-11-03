from interpretation_function.nary_tuple import NaryTuple
from interpretation_function.constant import Constant

from syntax.tokenizer import tokenize

from typing import List, Any, Optional


class Expr:
    pass


class QuantifierExpr(Expr):
    NAME = "Quantifier"

    def __init__(self, quantifier, variable, expr):
        self.quantifier = quantifier
        self.variable = variable
        self.expr = expr
        self.precedence = 4

    def __str__(self):
        return f"{self.quantifier}{self.variable}({self.expr})"


class PredicateExpr(Expr):
    NAME = "Predicate"

    def __init__(self, name, terms: List[Any]):
        self.name = name
        self.terms = NaryTuple(terms)
        self.precedence = 2
        self.evaluated_value: Optional[bool] = None

    def __str__(self):
        return f"{self.name}{self.terms}"


class NotExpr(Expr):
    NAME = "¬"

    def __init__(self, expr):
        self.expr = expr
        self.precedence = 3

    def __str__(self):
        return f"¬{self.expr}"


class AndExpr(Expr):
    NAME = "∧"

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.precedence = 6

    def __str__(self):
        return f"({self.left} ∧ {self.right})"


class OrExpr(Expr):
    NAME = "∨"

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.precedence = 7

    def __str__(self):
        return f"({self.left} ∨ {self.right})"


class ImpliesExpr(Expr):
    NAME = "→"

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.precedence = 8

    def __str__(self):
        return f"({self.left} → {self.right})"


class Parser:
    def __init__(self, formula: str, M):
        self.tokens = tokenize(formula)
        self.pos = 0
        self.interpretation = M.I

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
            return ImpliesExpr(left, right)
        return left

    def disjunct(self):
        left = self.conjunct()
        while self.peek() and self.peek().type == "OR":
            self.consume("OR")
            right = self.conjunct()
            left = OrExpr(left, right)
        return left

    def conjunct(self):
        left = self.quantified()
        while self.peek() and self.peek().type == "AND":
            self.consume("AND")
            right = self.quantified()
            left = AndExpr(left, right)
        return left

    def quantified(self):
        if self.peek() and self.peek().type == "QUANTIFIER":
            quantifier = self.consume("QUANTIFIER").value
            variable = self.consume("VARIABLE").value
            expr = self.quantified()
            return QuantifierExpr(quantifier, variable, expr)
        return self.negation()

    def negation(self):
        if self.peek() and self.peek().type == "NOT":
            self.consume("NOT")
            expr = self.negation()
            return NotExpr(expr)
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
            return PredicateExpr(name, terms)
        raise ValueError(f"Expected predicate but got {token}")

    def term(self):
        token = self.peek()
        if token.type == "VARIABLE":
            return self.consume("VARIABLE").value
        elif token.type == "CONSTANT":
            return self.consume("CONSTANT").value
        raise ValueError(f"Unexpected term token: {token}")
