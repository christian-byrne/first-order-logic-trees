from graphviz import Digraph
from PIL import Image
import os

from fol_ast import Expr, Predicate, Quantifier

def create_graph_image(node, level, current_level=0, graph=None, parent=None):
    if current_level > level:
        return
    if graph is None:
        graph = Digraph()
    
    label = str(node)
    graph.node(str(id(node)), label)
    
    if parent:
        graph.edge(str(id(parent)), str(id(node)))
    
    for child in getattr(node, '__dict__', {}).values():
        if isinstance(child, Expr):
            create_graph_image(child, level, current_level + 1, graph, node)
    
    return graph

def save_graph_image(node, level, filename):
    graph = create_graph_image(node, level)
    if graph:
        graph.render(filename, format="png")

def progressive_ast_images(ast, max_depth):
    images = []
    
    for level in range(max_depth + 1):
        filename = f"ast_level_{level}"
        save_graph_image(ast, level, filename)
        images.append(Image.open(f"{filename}.png"))
        if os.path.exists(f"{filename}.png"):
          os.remove(f"{filename}.png")  # Clean up temporary file
        if os.path.exists(f"{filename}"):
          os.remove(f"{filename}")   # Clean up Graphviz file
    
    return images

def stitch_images_horizontally(images):
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    
    stitched_image = Image.new("RGB", (total_width, max_height), (255, 255, 255))
    
    x_offset = 0
    for img in images:
        stitched_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    return stitched_image

def visualize_ast_progressively(ast, max_depth):
    images = progressive_ast_images(ast, max_depth)
    final_image = stitch_images_horizontally(images)
    final_image.show()
    final_image.save("output/progressive_ast.png")
