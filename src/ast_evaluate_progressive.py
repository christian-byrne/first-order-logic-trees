from graphviz import Digraph
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from typing import Any, List, Union

from fol_ast import And, Implies, Not, Or, Predicate, Quantifier, Expr
from ast_evaluate import evaluate
from ast_visualize_progressive import create_graph_image
from interpretation import Interpretation, Constant

Node = Union[Predicate, Not, And, Or, Implies, Quantifier, Expr]


# Step 1: Identify Nodes at Each Level
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


# Step 2: Evaluate Nodes at a Given Level with Captions
def evaluate_level(nodes: List[Node], interpretation: Interpretation) -> str:
    captions = []
    for node in nodes:
        if isinstance(node, Predicate):
            print(f"Evaluating Predicate: {node.name} with terms {node.terms}")
            node.evaluated_value = interpretation(node.name, tuple(node.terms))
            captions.append(
                f"Evaluated Predicate {node.name} with terms ({', '.join(node.terms)}) = {node.evaluated_value}"
            )

        elif isinstance(node, Not):
            node.evaluated_value = not node.expr.evaluated_value
            captions.append(f"Evaluated Not: ¬({node.expr}) = {node.evaluated_value}")

        elif isinstance(node, And):
            node.evaluated_value = (
                node.left.evaluated_value and node.right.evaluated_value
            )
            captions.append(
                f"Evaluated And: ({node.left} ∧ {node.right}) = {node.evaluated_value}"
            )

        elif isinstance(node, Or):
            node.evaluated_value = (
                node.left.evaluated_value or node.right.evaluated_value
            )
            captions.append(
                f"Evaluated Or: ({node.left} ∨ {node.right}) = {node.evaluated_value}"
            )

        elif isinstance(node, Implies):
            node.evaluated_value = (
                not node.left.evaluated_value or node.right.evaluated_value
            )
            captions.append(
                f"Evaluated Implies: ({node.left} → {node.right}) = {node.evaluated_value}"
            )

        elif isinstance(node, Quantifier):
            # Replace the quantifier node with True or False based on the domain and expression evaluation
            if node.quantifier == "∀":
                node.evaluated_value = all(
                    evaluate_with_binding(node.expr, interpretation, node.variable, obj)
                    for obj in interpretation.domain
                )
                captions.append(f"Evaluated ∀{node.variable}: {node.evaluated_value}")
            elif node.quantifier == "∃":
                node.evaluated_value = any(
                    evaluate_with_binding(node.expr, interpretation, node.variable, obj)
                    for obj in interpretation.domain
                )
                captions.append(f"Evaluated ∃{node.variable}: {node.evaluated_value}")

    return "; ".join(captions)


# Helper function to evaluate with a variable binding
def evaluate_with_binding(
    expr, interpretation: Interpretation, variable: str, value: Any
):
    print(f"Adding binding: {variable} -> {value}")
    interpretation.add_constant_object_mapping(Constant(variable), value)
    result = evaluate(expr, interpretation)
    interpretation.remove_constant_object_mapping(variable)
    return result


# Step 3: Generate Image of the AST at Each Level
def create_graph_image(node: Node, evaluated=True, graph=None):
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


# Step 4: Progressive Evaluation and Image Creation with Captions
def progressive_evaluation_images(ast: Expr, interpretation: Interpretation):
    images = []
    nodes_by_level = get_nodes_by_level(ast)

    # Start evaluating from the deepest level (max_depth) and move upwards
    for level in sorted(nodes_by_level.keys(), reverse=True):
        caption = evaluate_level(
            nodes_by_level[level], interpretation
        )  # Evaluate nodes and get caption

        # Create a graph image after each level evaluation
        graph = create_graph_image(ast)
        filename = f"progressive_eval_level_{level}"
        graph.render(filename, format="png")

        # Load the image and add the caption below it
        image = Image.open(f"{filename}.png")
        annotated_image = add_caption_below_image(image, caption)
        images.append(annotated_image)

        # Clean up temporary files
        if os.path.exists(f"{filename}.png"):
            os.remove(f"{filename}.png")
        if os.path.exists(f"{filename}.gv"):
            os.remove(f"{filename}.gv")
        if os.path.exists(f"{filename}"):
            os.remove(f"{filename}")

    return images



def add_caption_below_image(image: Image.Image, caption: str) -> Image.Image:
    # Load a Unicode-compatible font with logical symbols support
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)  # Adjust path and size as needed
    except IOError:
        font = ImageFont.load_default()  # Fallback if the TTF font is not found

    max_width = image.width  # Max width for line wrapping

    # Wrap text to fit within the max width
    draw = ImageDraw.Draw(image)
    lines = textwrap.wrap(caption, width=max_width // 10)  # Adjust width divisor as needed for wrapping

    # Calculate total height for all lines using textbbox
    line_height = draw.textbbox((0, 0), "A", font=font)[3]  # Height of a single line
    total_text_height = line_height * len(lines) + 10  # Add padding

    # Create a new image with extra height for the caption
    total_height = image.height + total_text_height
    annotated_image = Image.new("RGB", (image.width, total_height), "white")

    # Paste the original image on top
    annotated_image.paste(image, (0, 0))

    # Draw each line of wrapped text below the image
    draw = ImageDraw.Draw(annotated_image)
    y_text = image.height + 5
    for line in lines:
        text_width = draw.textbbox((0, 0), line, font=font)[2]  # Get width of each line
        draw.text(((image.width - text_width) // 2, y_text), line, fill="black", font=font)
        y_text += line_height

    return annotated_image


# Step 5: Stitch Images Horizontally
def stitch_images_horizontally(images: List[Image.Image]) -> Image.Image:
    # Determine the maximum height across all images
    max_height = max(img.height for img in images)
    total_width = sum(img.width for img in images)

    # Create a new blank (white) image with the total width and max height
    stitched_image = Image.new("RGB", (total_width, max_height), (255, 255, 255))

    # Paste each image onto the stitched image, centering vertically if shorter
    x_offset = 0
    for img in images:
        # If the image is shorter than max_height, create a white background
        if img.height < max_height:
            # Create a new image with white background and paste the original image on it
            extended_img = Image.new("RGB", (img.width, max_height), (255, 255, 255))
            extended_img.paste(img, (0, 0))
            stitched_image.paste(extended_img, (x_offset, 0))
        else:
            # If the image is already the correct height, paste it directly
            stitched_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return stitched_image


def visualize_progressive_evaluation(
    ast: Expr,
    interpretation: Interpretation,
    show_image=False,
    filename="progressive_evaluation.png",
) -> Image.Image:
    images = progressive_evaluation_images(ast, interpretation)
    final_image = stitch_images_horizontally(images)
    if show_image:
        final_image.show()
    final_image.save(f"../output/{filename}")
    return final_image
