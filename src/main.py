from rich import print
import os

from interpretation_function.predicate import Predicate
from interpretation_function.constant import Constant

from syntax.ast_evaluate import evaluate
from syntax.first_order_logic_syntax import Parser
from syntax.tokenizer import remap_symbols
from syntax.ast_evaluate_progressive import visualize_evaluation_progressively
from syntax.ast_visualize_progressive import visualize_ast_progressively

from utils.image_creation import (
    stitch_horizontal,
    create_interpretation_image,
    center_and_stitch_vertical,
)

from modal_logic.interpretation import Interpretation
from modal_logic.domain import DomainOfDiscourse
from modal_logic.model import Model

from utils.text_convert.to_latex import replace_symbols
from utils.text_convert.to_markdown import h

from utils.config import Config
from utils.log import Logger

config = Config()
logger = Logger(__name__, config["log_level"])()

EXAMPLE_FORMULAS = [
    "∀x(N(x) or !N(x))",
    "forall x (A(x) and B(x))",
    "exists x (A(x) and B(x))",
    "exists x (B(x)) -> forall x (A(x))",
    "∀x(N(x) or ∃y(Q(y) ∧ R(x, y)))",
]

M = (
    Model("M")
    .with_domain(DomainOfDiscourse("D").expand(["Corwin", "Benedict"]))
    .with_interpretation_function(
        Interpretation()
        .add_predicate(Predicate("A", 1).extend("Corwin").extend("Benedict"))
        .add_predicate(Predicate("B", 1).extend("Benedict"))
        .add_predicate(Predicate("N", 1))
        .extend(Constant("c"), "Corwin")
    )
)

formula = EXAMPLE_FORMULAS[0]

parser = Parser(formula, M)
ast = parser.parse()

trees_image = stitch_horizontal(
    [
        visualize_ast_progressively(ast),
        visualize_evaluation_progressively(ast, M),
    ]
)
final_image = center_and_stitch_vertical(
    [create_interpretation_image(M.I, trees_image.width), trees_image]
)
final_image.save("../output/formula_under_M.png")

result = evaluate(ast, M.I)
logger.warning(h("Final Result", 1))
logger.info(
    f"\n\nFormula {replace_symbols(remap_symbols(formula))} is {result} in {M.name}."
)

if config["auto_open_markdown_logs"]:
    os.system("pandoc ../annotated_proof.md -o ../annotated_proof.pdf")
    os.system("xdg-open ../annotated_proof.pdf")

final_image.show()
