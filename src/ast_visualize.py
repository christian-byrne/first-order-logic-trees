from graphviz import Digraph

from fol_ast import Expr, Predicate, Quantifier


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
    for child in getattr(node, '__dict__', {}).values():
        if isinstance(child, Expr):
            visualize_ast(child, graph, node)
    
    return graph
