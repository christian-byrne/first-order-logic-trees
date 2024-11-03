from typing import List, Dict, Union

from fol_ast import Expr, Predicate, Quantifier, Not, And, Or, Implies

Node = Union[Predicate, Quantifier, Expr, Not, And, Or, Implies]


def get_nodes_by_level(node: Node, nodes_by_level: dict = None, level=0):
    if nodes_by_level is None:
        nodes_by_level = {}
    if level not in nodes_by_level:
        nodes_by_level[level] = []
    nodes_by_level[level].append(node)

    # Recursively collect nodes in child expressions
    for child in getattr(node, "__dict__", {}).values():
        if isinstance(child, Expr):
            get_nodes_by_level(child, nodes_by_level, level + 1)

    return nodes_by_level
