
From *forall x* p. 275

```python
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

EXAMPLE_FORMULAS = [
    "∀x(N(x) or !N(x))",
    "forall x (A(x) and B(x))",
    "exists x (A(x) and B(x))",
    "exists x (B(x)) -> forall x (A(x))",
    "∀x(N(x) or ∃y(Q(y) ∧ R(x, y)))",
]
```