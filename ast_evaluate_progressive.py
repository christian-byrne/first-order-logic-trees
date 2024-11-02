from graphviz import Digraph
from PIL import Image
import os

from fol_ast import And, Implies, Not, Or, Predicate, Quantifier, Expr
from ast_evaluate import evaluate
from ast_visualize_progressive import create_graph_image
from interpretation import Interpretation, Constant

from typing import Any, List


# Step 1: Identify Nodes at Each Level
def get_nodes_by_level(node, nodes_by_level=None, level=0):
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


# Step 2: Evaluate Nodes at a Given Level
def evaluate_level(nodes, interpretation):
    for node in nodes:
        if isinstance(node, Predicate):
            node.evaluated_value = interpretation(node.name)(tuple(node.terms))

        elif isinstance(node, Not):
            node.evaluated_value = not node.expr.evaluated_value
        
        elif isinstance(node, And):
            node.evaluated_value = (
                node.left.evaluated_value and node.right.evaluated_value
            )
        
        elif isinstance(node, Or):
            node.evaluated_value = (
                node.left.evaluated_value or node.right.evaluated_value
            )
        
        elif isinstance(node, Implies):
            node.evaluated_value = (
                not node.left.evaluated_value or node.right.evaluated_value
            )
        
        elif isinstance(node, Quantifier):
            # Replace the quantifier node with True or False based on the domain and expression evaluation
            if node.quantifier == "∀":
                node.evaluated_value = all(
                    evaluate_with_binding(node.expr, interpretation, node.variable, obj)
                    for obj in interpretation.domain
                )
            elif node.quantifier == "∃":
                node.evaluated_value = any(
                    evaluate_with_binding(node.expr, interpretation, node.variable, obj)
                    for obj in interpretation.domain
                )


# Helper function to evaluate with a variable binding
def evaluate_with_binding(expr, interpretation: Interpretation, variable: str, value: Any):
    interpretation.add_constant_object_mapping(Constant(variable), value)
    result = evaluate(expr, interpretation)
    interpretation.remove_constant_object_mapping(variable)
    return result


# Step 3: Generate Image of the AST at Each Level
def create_graph_image(node, evaluated=True, graph=None):
    if graph is None:
        graph = Digraph()

    label = (
        str(node.evaluated_value)
        if evaluated and hasattr(node, "evaluated_value")
        else str(node)
    )
    graph.node(str(id(node)), label)

    for child in getattr(node, "__dict__", {}).values():
        if isinstance(child, Expr):
            graph.edge(str(id(node)), str(id(child)))
            create_graph_image(child, evaluated, graph)

    return graph


# Step 4: Progressive Evaluation and Image Creation
def progressive_evaluation_images(ast, interpretation, max_depth):
    images = []
    nodes_by_level = get_nodes_by_level(ast)

    # Start evaluating from the deepest level (max_depth) and move upwards
    for level in sorted(nodes_by_level.keys(), reverse=True):
        evaluate_level(
            nodes_by_level[level], interpretation
        )  # Evaluate nodes at the current level

        # Create a graph image after each level evaluation
        graph = create_graph_image(ast)
        filename = f"progressive_eval_level_{level}"
        graph.render(filename, format="png")

        # Add the rendered image to the images list
        images.append(Image.open(f"{filename}.png"))

        if os.path.exists(f"{filename}.png"):
          os.remove(f"{filename}.png")  # Clean up temporary file
        if os.path.exists(f"{filename}.gv"):
          os.remove(f"{filename}.gv")  # Clean up Graphviz file
        if os.path.exists(f"{filename}"):
          os.remove(f"{filename}")  # Clean up Graphviz file

    return images


# Step 5: Stitch Images Horizontally
def stitch_images_horizontally(images: List[Image.Image]) -> Image.Image:
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    stitched_image = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for img in images:
        stitched_image.paste(img, (x_offset, 0))
        x_offset += img.width
    return stitched_image


def visualize_progressive_evaluation(ast, interpretation):
    max_depth = max(get_nodes_by_level(ast).keys())
    images = progressive_evaluation_images(ast, interpretation, max_depth)
    final_image = stitch_images_horizontally(images)
    final_image.show()
    final_image.save("progressive_evaluation.png")
