from graphviz import Digraph
from PIL import Image
from typing import Any, List, Union, Tuple

from syntax.first_order_logic_syntax import (
    AndExpr,
    ImpliesExpr,
    NotExpr,
    OrExpr,
    PredicateExpr,
    QuantifierExpr,
    Expr,
)
from syntax.ast_evaluate import evaluate
from syntax.ast_visualize_progressive import create_graph_image
from syntax.ast_utils import get_nodes_by_level

from interpretation_function.constant import Constant
from interpretation_function.variable import Variable

from modal_logic.model import Model

from utils.files import cleanup_temp_files
from utils.image_creation import add_caption_below_image, save_image

from utils.text_convert.to_latex import t, im, mm, st, symb, symb_sub, replace_symbols
from utils.text_convert.to_markdown import df, h

from utils.config import Config
from utils.log import Logger


config = Config()
logger = Logger(__name__, config["log_level"])()

Node = Union[PredicateExpr, NotExpr, AndExpr, OrExpr, ImpliesExpr, QuantifierExpr, Expr]


# Step 1: Identify Nodes at Each Level
levels_with_full_explanations = set()


# Step 2: Evaluate Nodes at a Given Level with Captions
def evaluate_level(
    nodes: List[Node],
    M: Model,
    cur_lvl: int,
    total_lvls: int,
) -> str:
    captions = []
    for node in nodes:
        explanation_title = f"Evaluated AST - Level {total_lvls - cur_lvl}\n\n"
        explanation = ""
        if cur_lvl not in levels_with_full_explanations:
            logger.info(h(explanation_title, 2))
        if isinstance(node, PredicateExpr):
            predicate = M.I(node)
            node.evaluated_value = predicate(node.terms, M.I)
            explanation += predicate.explain_evaluation(
                M.I, node.terms, cur_lvl in levels_with_full_explanations
            )
            captions.append(explanation)
            levels_with_full_explanations.add(cur_lvl)

        elif isinstance(node, NotExpr):
            node.evaluated_value = not node.expr.evaluated_value
            explanation += (
                f"¬{node.expr} is true in interpretation {M.name}"
                + f" iff {node.expr} is false in {M.I.name}\n\n"
                + f" ¬({node.expr}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, AndExpr):
            node.evaluated_value = (
                node.left.evaluated_value and node.right.evaluated_value
            )
            explanation += (
                f"{node.left} ∧ {node.right} is true in interpretation {M.name}"
                + f" iff both {node.left} is true and {node.right} is true in"
                + f" {M.name}\n\n"
                + f" ({node.left} ∧ {node.right}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, OrExpr):
            node.evaluated_value = (
                node.left.evaluated_value or node.right.evaluated_value
            )
            explanation += (
                f"{node.left} ∨ {node.right} is true in interpretation {M.name}"
                + f" iff either {node.left} is true or {node.right} is true in"
                + f" {M.name}\n\n"
                + f" ({node.left} ∨ {node.right}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, ImpliesExpr):
            node.evaluated_value = (
                not node.left.evaluated_value or node.right.evaluated_value
            )
            reasons = []
            if not node.left.evaluated_value:
                reasons.append(f"{node.left} is False in {M.name}")
            if node.right.evaluated_value:
                reasons.append(f"{node.right} is True in {M.name}")
            if reasons:
                reason = ", ".join(reasons)
            else:
                reason = f"({node.left} is True in {M.I.name}) ∧ ({node.right} is False in {M.name})"

            explanation += (
                f"{node.left} → {node.right} is true in {M.name} under interpretation {M.I.name}"
                + f" iff either {node.left} is false or {node.right} is true in"
                + f" {M.name}\n\n"
                + f"{reason}\n\n"
                + f" ({node.left} → {node.right}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, QuantifierExpr):
            max_length = 5
            abbreviated_domain = [str(obj) for obj in M.I.domain][
                :max_length
            ]
            if len(M.I.domain) > max_length:
                abbreviated_domain.append("...")
            abbreviated_domain = "{" + ", ".join(abbreviated_domain) + "}"

            # Replace the quantifier node with True or False based on the domain and expression evaluation
            if node.quantifier == "∀":
                evaluations: List[Tuple[bool, Any]] = []
                for d_obj in M.universal_instantiation(Variable(node.variable)):
                    res = evaluate(node.expr, M.I)
                    evaluations.append((res, d_obj))
                    logger.debug(f"{node.variable} = {d_obj} satisfies {node.expr}: {res}")

                node.evaluated_value = all(result[0] for result in evaluations)
                failed_evaluations = [
                    f"{node.variable} = {obj} does not satisfy {node.expr}"
                    for result, obj in evaluations
                    if not result
                ]
                result_str = f"{node.expr} ⟷ {node.evaluated_value} for all objects in {M.name}'s domain"
                if not node.evaluated_value:
                    result_str = ", ".join(failed_evaluations)

                explanation += (
                    f"{node.quantifier}{node.variable}({node.expr}) is true in {M.name} under {M.I.name}"
                    + f" iff every object in {M.I.name}'s domain"
                    + f" ({abbreviated_domain}) satisfies {node.expr}\n\n"
                    + f"{result_str}\n\n"
                    + f"{node.quantifier}{node.variable}({node.expr}) ⟷ {node.evaluated_value}\n\n"
                )
                captions.append(explanation)

            elif node.quantifier == "∃":
                evaluations: List[Tuple[bool, Any]] = []
                for d_obj in M.universal_instantiation(Variable(node.variable)):
                    res = evaluate(node.expr, M.I)
                    evaluations.append((res, d_obj))
                    logger.debug(f"{node.variable} = {d_obj} satisfies {node.expr}: {res}")

                node.evaluated_value = any(result[0] for result in evaluations)
                successful_evaluations = [
                    f"{M.I.name}({node.variable}) = '{obj}' satisfies {node.expr}"
                    for result, obj in evaluations
                    if result
                ]
                explanation += (
                    f"{node.quantifier}{node.variable}({node.expr}) is true in {M.name} under {M.I.name}"
                    + f" iff at least one object in {M.I.name}'s domain"
                    + f" ({abbreviated_domain}) satisfies {node.expr}\n\n"
                    + f"{', '.join(successful_evaluations)}\n\n"
                    + f"{node.quantifier}{node.variable}({node.expr}) ⟷ {node.evaluated_value}\n\n"
                )
                captions.append(explanation)

    logger.info(replace_symbols("\n".join(captions)))
    return "".join([explanation_title] + captions)


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
def progressive_evaluation_images(ast: Expr, M: Model):
    images = []
    nodes_by_level = get_nodes_by_level(ast)
    total_levels = len(nodes_by_level)

    # Start evaluating from the deepest level (max_depth) and move upwards
    for level_num, level in enumerate(sorted(nodes_by_level.keys(), reverse=True)):
        caption = evaluate_level(
            nodes_by_level[level], M, level_num, total_levels
        )  # Evaluate nodes and get caption

        # Create a graph image after each level evaluation
        graph = create_graph_image(ast)
        filename = config.get_proj_root() / "output" / f"progressive_eval_level_{level}"
        graph.render(filename, format="png")

        # Load the image and add the caption below it
        image = Image.open(f"{filename}.png")
        annotated_image = add_caption_below_image(
            image, caption, level_count=total_levels
        )
        images.append(annotated_image)
        # cleanup_temp_files(filename)

    return images


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


def visualize_evaluation_progressively(
    ast: Expr,
    M: Model,
    show_image=False,
    filename="progressive_evaluation.png",
) -> Image.Image:
    images = progressive_evaluation_images(ast, M)
    final_image = stitch_images_horizontally(images)
    if show_image:
        final_image.show()
    save_image(final_image, filename)
    return final_image
