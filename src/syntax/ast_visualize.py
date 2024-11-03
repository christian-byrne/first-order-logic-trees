from graphviz import Digraph

from syntax.first_order_logic_syntax import Expr


def visualize_ast(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph()

    # Use `str(node)` to get the descriptive label
    label = str(node)
    graph.node(str(id(node)), label)

    # Connect to the parent node
    if parent:
        graph.edge(str(id(parent)), str(id(node)))

    # Recursively add children nodes
    for child in getattr(node, "__dict__", {}).values():
        if isinstance(child, Expr):
            visualize_ast(child, graph, node)

    return graph
