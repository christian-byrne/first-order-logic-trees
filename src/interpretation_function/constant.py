from typing import Union


class Constant:
    """
    A constant is a symbol that represents a specific object in the domain. In FOL, constants are used to refer to specific individuals, objects, or entities within the domain. Each constant is assigned a unique name or label that identifies the object it represents.

    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: Union["Constant", str]):
        if isinstance(other, Constant):
            return self.name == other.name
        return self.name == other
