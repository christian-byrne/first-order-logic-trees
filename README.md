

![image example](./output/formula_under_interpretation.example.png)


```python
I_a = (
    Interpretation()
    .add_to_domain(["Corwin", "Benedict"])
    .add_predicate(Predicate("A", 1).extend("Corwin").extend("Benedict"))
    .add_predicate(Predicate("B", 1).extend("Benedict"))
    .add_predicate(Predicate("N", 1))
    .add_constant_object_mapping(Constant("c"), "Corwin")
)

formula = remap_symbols("∀x(N(x) or !N(x))")

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
final_image.save("output/formula_under_interpretation.png")
```