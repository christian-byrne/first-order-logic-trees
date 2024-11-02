from interpretation import Interpretation, Predicate, Constant
from fol_ast import Parser, tokenize
from ast_evaluate import evaluate
from ast_visualize import visualize_ast
from ast_visualize_progressive import visualize_ast_progressively
from ast_evaluate_progressive import visualize_progressive_evaluation

from PIL import Image

I_a = (
    Interpretation()
    .add_to_domain(["Corwin", "Benedict"])
    .add_predicate(Predicate("A", 1).extend("Corwin").extend("Benedict"))
    .add_predicate(Predicate("B", 1).extend("Benedict"))
    .add_predicate(Predicate("N", 1))
    .add_constant_object_mapping(Constant("c"), "Corwin")
)

symbol_remap = {
    "or": "∨",
    "|": "∨",
    "and": "∧",
    "&": "∧",
    "&&": "∧",
    "not": "¬",
    "!": "¬",
    "implies": "→",
    "=>": "→",
    "->": "→",
    "—>": "→",
    "forall": "∀",
    "exists": "∃",
}


def remap_symbols(formula):
    for symbol, replacement in symbol_remap.items():
        while symbol in formula:
            formula = formula.replace(symbol, replacement)
    print(f"Remapped formula: {formula}")
    return formula


formula = "∀x(N(x) or !N(x))"
# formula = "∀x(N(x) or ∃y(Q(y) ∧ R(x, y)))"

formula = remap_symbols(formula)
tokens = tokenize(formula)
parser = Parser(tokens, I_a)
ast = parser.parse()
# ast_graph = visualize_ast(ast)  # Assuming `ast` is your AST root node
# ast_graph.render("ast_tree", format="png", view=True)  # Save and view the image

res = evaluate(ast, I_a)  # Should evaluate the formula under the interpretation

def combine_images_on_nice_bg(images):
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im

ast_image = visualize_ast_progressively(ast, 3, show_image=False)
eval_image = visualize_progressive_evaluation(ast, I_a, show_image=False)

combined_image = combine_images_on_nice_bg([ast_image, eval_image])
combined_image.show()

