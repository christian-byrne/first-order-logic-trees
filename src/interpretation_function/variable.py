from typing import Union


class Variable:
    """
    A variable is a symbol that represents a placeholder or a generic object in the domain. In FOL, variables are used to represent objects that are not explicitly named or identified. Variables are placeholders that can be replaced by constants or other objects during the evaluation of logical expressions.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: Union["Variable", str]):
        if isinstance(other, Variable):
            return self.name == other.name
        return self.name == other
