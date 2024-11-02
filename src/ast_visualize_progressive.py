from graphviz import Digraph
import textwrap
from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Union

from fol_ast import Expr, Predicate, Quantifier, Not, And, Or, Implies

Node = Union[Predicate, Quantifier, Expr, Not, And, Or, Implies]

# Function to create an image of the AST up to a specific depth level
def create_graph_image(
    node: Node,
    level: int,
    current_level: int = 0,
    graph: Digraph = None,
    parent: Node = None,
) -> Digraph:
    if current_level > level:
        return
    if graph is None:
        graph = Digraph()

    label = str(node)
    graph.node(str(id(node)), label)

    if parent:
        graph.edge(str(id(parent)), str(id(node)))

    for child in getattr(node, "__dict__", {}).values():
        if isinstance(child, Expr):
            create_graph_image(child, level, current_level + 1, graph, node)

    return graph

# Function to save the graph image for a specific depth level
def save_graph_image(node: Node, level: int, filename: str) -> None:
    graph = create_graph_image(node, level)
    if graph:
        graph.render(filename, format="png")

# Function to generate images of the AST being built progressively level by level
def progressive_ast_images(ast: Expr, max_depth: int) -> List[Image.Image]:
    images = []

    for level in range(max_depth + 1):
        filename = f"ast_level_{level}"
        save_graph_image(ast, level, filename)
        image = Image.open(f"{filename}.png")

        # Add a caption describing the current level
        caption = f"Building AST - Level {level}"
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

# Function to add a caption below an image
def add_caption_below_image(image: Image.Image, caption: str) -> Image.Image:
    # Load a Unicode-compatible font with support for logical symbols
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except IOError:
        font = ImageFont.load_default()  # Fallback if TTF font is unavailable

    max_width = image.width

    # Wrap text to fit within max width
    draw = ImageDraw.Draw(image)
    lines = textwrap.wrap(caption, width=max_width // 10)

    # Calculate total height for all lines
    line_height = draw.textbbox((0, 0), "A", font=font)[3]
    total_text_height = line_height * len(lines) + 10

    # Create a new image with extra height for the caption
    total_height = image.height + total_text_height
    annotated_image = Image.new("RGB", (image.width, total_height), (255, 255, 255))

    # Paste the original image on top
    annotated_image.paste(image, (0, 0))

    # Draw each line of wrapped text below the image
    draw = ImageDraw.Draw(annotated_image)
    y_text = image.height + 5
    for line in lines:
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        draw.text(((image.width - text_width) // 2, y_text), line, fill="black", font=font)
        y_text += line_height

    return annotated_image

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
    max_depth: int,
    show_image: bool = False,
    filename: str = "progressive_ast.png",
) -> Image.Image:
    images = progressive_ast_images(ast, max_depth)
    final_image = stitch_images_horizontally(images)
    if show_image:
        final_image.show()
    final_image.save(f"../output/{filename}")
    return final_image
