from typing import Union

from syntax.first_order_logic_syntax import (
    Expr,
    PredicateExpr,
    QuantifierExpr,
    NotExpr,
    AndExpr,
    OrExpr,
    ImpliesExpr,
)

Node = Union[PredicateExpr, QuantifierExpr, Expr, NotExpr, AndExpr, OrExpr, ImpliesExpr]


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
