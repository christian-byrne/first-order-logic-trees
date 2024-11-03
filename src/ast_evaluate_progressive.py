from graphviz import Digraph
from PIL import Image
import os
from typing import Any, List, Union, Tuple

from fol_ast import And, Implies, Not, Or, Predicate, Quantifier, Expr
from ast_evaluate import evaluate
from ast_visualize_progressive import create_graph_image
from ast_utils import get_nodes_by_level

from interpretation import Interpretation, Constant
from image_creation import add_caption_below_image

Node = Union[Predicate, Not, And, Or, Implies, Quantifier, Expr]


# Step 1: Identify Nodes at Each Level
levels_with_full_explanations = set()


def format_predicate(
    predicate_name: str, terms: List[str], evaluated_terms: List[str]
) -> Tuple[str, str]:
    if len(terms) == 0:
        return f"{predicate_name}()", f"{predicate_name}()"
    if len(terms) == 1:
        return (
            f"{predicate_name}({terms[0]})",
            f"{predicate_name}({evaluated_terms[0]})",
        )
    return (
        f"{predicate_name}(...{'...'.join(terms)}...)",
        f"{predicate_name}(...{'...'.join(evaluated_terms)}...)",
    )


def format_mapping(predicate_objs: List[str]) -> Tuple[str, str]:
    if len(predicate_objs) == 0:
        return "", ""
    if len(predicate_objs) == 1:
        return "d", predicate_objs[0]
    alphabet = "defghijklmnopqrstuvwxyzabc"
    letters = [alphabet[i] for i in range(len(predicate_objs))]
    return f"{', '.join(letters)}", f"{', '.join(predicate_objs)}"


# Step 2: Evaluate Nodes at a Given Level with Captions
def evaluate_level(
    nodes: List[Node],
    interpretation: Interpretation,
    current_lvl_num: int,
    max_levels: int,
) -> str:
    captions = []
    for node in nodes:
        explanation = f"Evaluated AST - Level {max_levels - current_lvl_num}\n\n"
        if isinstance(node, Predicate):
            node.evaluated_value = interpretation(node.name, tuple(node.terms))
            resolved_terms = []
            for term in node.terms:
                resolved_terms.append(interpretation(term))

            terms_under_I = [f"I({term})" for term in node.terms]
            A_x, A_c = format_predicate(node.name, node.terms, resolved_terms)
            d, c = format_mapping(resolved_terms)

            short_explanation = (
                f" {interpretation.name}({node.name}) ="
                + f" {interpretation.predicates[node.name].true_for}\n\n"
                + f" {', '.join(resolved_terms)} ∈ {interpretation.predicates[node.name].true_for}"
                + f" = {node.evaluated_value}\n\n"
            )
            preamble = (
                f"An object {d} satisfies {A_x}"
                + f" in interpretation {interpretation.name}"
                + f" iff {A_c}"
                + f" is true in {interpretation.name}[{d}/{c}]\n\n"
                + f"To evaluate predicate {node.name} with terms {', '.join(node.terms)},"
                + f" resolve terms under {interpretation.name}:\n"
                + f"{', '.join(terms_under_I)} = {', '.join(resolved_terms)}\n\n"
                + f"Then, find {node.name}({', '.join(resolved_terms)})"
                + f" by determining if {', '.join(resolved_terms)} ∈ the "
                + f" set of ordered pairs mapped to by {interpretation.name}({node.name})\n\n"
            )
            if current_lvl_num not in levels_with_full_explanations:
                explanation += preamble + short_explanation
                levels_with_full_explanations.add(current_lvl_num)
            else:
                explanation += short_explanation

            captions.append(explanation)

        elif isinstance(node, Not):
            node.evaluated_value = not node.expr.evaluated_value
            explanation += (
                f"¬{node.expr} is true in interpretation {interpretation.name}"
                + f" iff {node.expr} is false in {interpretation.name}\n\n"
                + f" ¬({node.expr}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, And):
            node.evaluated_value = (
                node.left.evaluated_value and node.right.evaluated_value
            )
            explanation += (
                f"{node.left} ∧ {node.right} is true in interpretation {interpretation.name}"
                + f" iff both {node.left} is true and {node.right} is true in"
                + f" {interpretation.name}\n\n"
                + f" ({node.left} ∧ {node.right}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, Or):
            node.evaluated_value = (
                node.left.evaluated_value or node.right.evaluated_value
            )
            explanation += (
                f"{node.left} ∨ {node.right} is true in interpretation {interpretation.name}"
                + f" iff either {node.left} is true or {node.right} is true in"
                + f" {interpretation.name}\n\n"
                + f" ({node.left} ∨ {node.right}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, Implies):
            node.evaluated_value = (
                not node.left.evaluated_value or node.right.evaluated_value
            )
            explanation += (
                f"{node.left} → {node.right} is true in interpretation {interpretation.name}"
                + f" iff either {node.left} is false or {node.right} is true in"
                + f" {interpretation.name}\n\n"
                + f" ({node.left} → {node.right}) = {node.evaluated_value}\n\n"
            )
            captions.append(explanation)

        elif isinstance(node, Quantifier):
            max_length = 5
            abbreviated_domain = [str(obj) for obj in interpretation.domain][
                :max_length
            ]
            if len(interpretation.domain) > max_length:
                abbreviated_domain.append("...")
            abbreviated_domain = "{" + ", ".join(abbreviated_domain) + "}"

            # Replace the quantifier node with True or False based on the domain and expression evaluation
            if node.quantifier == "∀":
                evaluations = [
                    evaluate_with_binding(node.expr, interpretation, node.variable, obj)
                    for obj in interpretation.domain
                ]
                node.evaluated_value = all(result[0] for result in evaluations)
                failed_evaluations = [
                    f"{node.variable} = {obj} does not satisfy {node.expr}"
                    for result, obj in evaluations
                    if not result
                ]
                result_str = ""
                if node.evaluated_value:
                    result_str = ", ".join(failed_evaluations)
                else:
                    result_str = f"{node.expr} ⟷ {node.evaluated_value} for all objects in {interpretation.name}'s domain"
                explanation += (
                    f"{node.quantifier}{node.variable}({node.expr}) is true in {interpretation.name}"
                    + f" iff every object in {interpretation.name}'s domain"
                    + f" ({abbreviated_domain}) satisfies {node.expr}\n\n"
                    + result_str
                    + f"{node.quantifier}{node.variable} ⟷ {node.evaluated_value}\n\n"
                )
                captions.append(explanation)

            elif node.quantifier == "∃":
                evaluations = [
                    evaluate_with_binding(node.expr, interpretation, node.variable, obj)
                    for obj in interpretation.domain
                ]
                node.evaluated_value = any(result[0] for result in evaluations)
                successful_evaluations = [
                    f"{interpretation.name}({node.variable}) = {obj} satisfies {node.expr}"
                    for result, obj in evaluations
                    if result
                ]
                explanation += (
                    f"{node.quantifier}{node.variable}({node.expr}) is true in {interpretation.name}"
                    + f" iff at least one object in {interpretation.name}'s domain"
                    + f" ({abbreviated_domain}) satisfies {node.expr}\n\n"
                    + f"{', '.join(successful_evaluations)}\n\n"
                    + f"{node.quantifier}{node.variable}({node.expr}) ⟷ {node.evaluated_value}\n\n"
                )
                captions.append(explanation)

    return "".join(captions)


# Helper function to evaluate with a variable binding
def evaluate_with_binding(
    expr, interpretation: Interpretation, variable: str, value: Any
):
    interpretation.add_constant_object_mapping(Constant(variable), value)
    result = evaluate(expr, interpretation)
    interpretation.remove_constant_object_mapping(variable)
    return result, value


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
    total_levels = len(nodes_by_level)

    # Start evaluating from the deepest level (max_depth) and move upwards
    for level_num, level in enumerate(sorted(nodes_by_level.keys(), reverse=True)):
        caption = evaluate_level(
            nodes_by_level[level], interpretation, level_num, total_levels
        )  # Evaluate nodes and get caption

        # Create a graph image after each level evaluation
        graph = create_graph_image(ast)
        filename = f"progressive_eval_level_{level}"
        graph.render(filename, format="png")

        # Load the image and add the caption below it
        image = Image.open(f"{filename}.png")
        annotated_image = add_caption_below_image(
            image, caption, level_count=total_levels
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
