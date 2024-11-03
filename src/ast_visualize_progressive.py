from graphviz import Digraph
from PIL import Image
import os
from typing import List, Union, Tuple

from fol_ast import Expr, Predicate, Quantifier, Not, And, Or, Implies
from image_creation import add_caption_below_image
from ast_utils import get_nodes_by_level

Node = Union[Predicate, Quantifier, Expr, Not, And, Or, Implies]


# Function to create an image of the AST up to a specific depth level
def create_graph_image(
    node: Node,
    level: int,
    current_level: int = 0,
    graph: Digraph = None,
    parent: Node = None,
) -> Tuple[Digraph, List[Node]]:
    if current_level > level:
        return
    if graph is None:
        graph = Digraph()

    label = str(node)
    graph.node(str(id(node)), label)

    ret_node = [node]
    if parent:
        graph.edge(str(id(parent)), str(id(node)))

    for child in getattr(node, "__dict__", {}).values():
        if isinstance(child, Expr):
            x = create_graph_image(child, level, current_level + 1, graph, node)
            if x:
                ret_node = x[1]

    return graph, ret_node


# Function to save the graph image for a specific depth level
def save_graph_image(node: Node, level: int, filename: str) -> List[Node]:
    graph, node_result = create_graph_image(node, level)
    if graph:
        graph.render(filename, format="png")
    return node_result


# Function to generate images of the AST being built progressively level by level
def progressive_ast_images(ast: Expr) -> List[Image.Image]:
    images = []
    nodes_by_level = get_nodes_by_level(ast)
    level_count = len(nodes_by_level)

    for level in range(level_count):
        filename = f"ast_level_{level}"
        target_node = save_graph_image(ast, level, filename)
        image = Image.open(f"{filename}.png")

        caption = f"Built AST - Level {level + 1}\n\n"

        # If there are multiple nodes, get all of them
        if len(nodes_by_level[level]) > 1:
            for index, node in enumerate(nodes_by_level[level]):
                caption += (
                    f"Term {index + 1}:"
                    + f" {str(node)}\n"
                    + f"Main Logical Operator: {type(node).__name__}\n"
                    + f"Precedence: {getattr(node, 'precedence', 'N/A')}\n\n"
                )

        else:
            caption += (
                f"{str(target_node[0])}\n"
                + f"Main Logical Operator: {type(target_node[0]).__name__}\n"
                + f"Precedence: {getattr(target_node[0], 'precedence', 'N/A')}\n\n"
            )

        annotated_image = add_caption_below_image(
            image, caption, level_count=level_count
        )
        images.append(annotated_image)

        # Clean up temporary files
        if os.path.exists(f"{filename}.png"):
            os.remove(f"{filename}.png")
        if os.path.exists(f"{filename}.gv"):
            os.remove(f"{filename}.gv")
        if os.path.exists(f"{filename}"):
            os.remove(f"{filename}")

    return images


# Function to stitch images horizontally
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


# Main function to visualize the AST being built progressively
def visualize_ast_progressively(
    ast: Expr,
    show_image: bool = False,
    filename: str = "progressive_ast.png",
) -> Image.Image:
    images = progressive_ast_images(ast)
    final_image = stitch_images_horizontally(images)
    if show_image:
        final_image.show()
    final_image.save(f"../output/{filename}")
    return final_image
