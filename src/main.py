from interpretation import Interpretation, Predicate, Constant

from fol_ast import Parser, tokenize

from ast_evaluate import evaluate
from ast_evaluate_progressive import visualize_progressive_evaluation
from ast_visualize_progressive import visualize_ast_progressively

from image_creation import (
    stitch_horizontal,
    create_interpretation_image,
    center_and_stitch_vertical,
)

symbol_remap = {
    "forall": "∀",
    "exists": "∃",
    "|": "∨",
    "&": "∧",
    "&&": "∧",
    "not": "¬",
    "!": "¬",
    "implies": "→",
    "=>": "→",
    "->": "→",
    "—>": "→",
    "and": "∧",
    "or": "∨",
}


def remap_symbols(formula):
    for symbol, replacement in symbol_remap.items():
        while symbol in formula:
            formula = formula.replace(symbol, replacement)
    print(f"Remapped formula: {formula}")
    return formula


# formula = "∀x(N(x) or ∃y(Q(y) ∧ R(x, y)))"
# ast_graph = visualize_ast(ast)  # Assuming `ast` is your AST root node
# ast_graph.render("ast_tree", format="png", view=True)  # Save and view the image
# res = evaluate(ast, I_a)  # Should evaluate the formula under the interpretation

I_a = (
    Interpretation()
    .add_to_domain(["Corwin", "Benedict"])
    .add_predicate(Predicate("A", 1).extend("Corwin").extend("Benedict"))
    .add_predicate(Predicate("B", 1).extend("Benedict"))
    .add_predicate(Predicate("N", 1))
    .add_constant_object_mapping(Constant("c"), "Corwin")
)

formula = remap_symbols("∀x(N(x) or !N(x))")
# formula = remap_symbols("exists x (B(x)) -> forall x (A(x))")

tokens = tokenize(formula)
parser = Parser(tokens, I_a)
ast = parser.parse()

trees_image = stitch_horizontal(
    [
        visualize_ast_progressively(ast, 3, show_image=False),
        visualize_progressive_evaluation(ast, I_a, show_image=False),
    ]
)
final_image = center_and_stitch_vertical(
    [create_interpretation_image(I_a, trees_image.width), trees_image]
)
final_image.save("../output/formula_under_interpretation.png")
final_image.show()
