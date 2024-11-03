import itertools

from .nary_tuple import NaryTuple
from modal_logic.interpretation import Interpretation


class Predicate:
    """
    A predicate is a function that takes objects as arguments and returns a truth value. In FOL, predicates are used to describe properties or relationships between objects in the domain. Predicates can have multiple arguments, and the truth value of the predicate is determined by the objects assigned to these arguments in the interpretation.

    """

    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity
        self.true_for = []
        self.is_unary = arity == 1

    def __str__(self):
        return self.name

    def __call__(self, objects: NaryTuple, interpretation: Interpretation):
        return objects.get_resolved_terms(interpretation) in self.true_for

    def extend(self, objects):
        if isinstance(objects, (list, tuple, set)):
            self.true_for.append(NaryTuple(objects))
        elif isinstance(objects, str):
            self.true_for.append(NaryTuple([objects]))
        else:
            raise ValueError(
                f"Predicate {self.name} expects a string or list of strings as arguments."
            )
        return self

    def represent_extension(self):
        return "{" + ", ".join([f"{term}" for term in self.true_for]) + "}"

    def represent_domain_permutations(self, interpretation: Interpretation, max_permutations=None):
        if max_permutations is None:
            max_permutations = int(self.arity * 2.5)

        domain_permutations = list(itertools.product(interpretation.domain, repeat=self.arity))
        for domain_object in interpretation.domain:
            domain_permutations.append(
                f"{self.name}({domain_object}) = {self(NaryTuple([domain_object]), interpretation)}"
            )
        return domain_permutations

    def represent_satisfying_condition(
        self, input_tuple: NaryTuple, interpretation: Interpretation
    ) -> str:
        lines = [
            f"Find {self}{input_tuple}",
            f"by determining if {input_tuple} ∈",
            f"{interpretation.name}({self}) =",
            f"the set of tuples from the domain of {interpretation.name} that",
            f"satisfy the predicate {str(self)[0]} under {interpretation.name}.",
            "\n\n",
        ]
        if self.is_unary:
            lines.append(
                f"Since {self} is a unary predicate,",
                f"{interpretation.name}({self}) ⊆ {interpretation.domain_name}",
                f"would be the subset of elements in {interpretation.domain_name}",
                f"for which {self} holds.",
                "\n\n",
            )
        else:
            cartesian_product_str = " × ".join(
                [f"{interpretation.domain_name}"] * self.arity
            )
            permutations = [] 
            lines.extend([
                f"Since {self} is a {self.arity}-ary predicate,",
                f"{interpretation.name}({self}) ⊆ {cartesian_product_str}",
                f"would be the set of tuples of {self.arity} elements in",
                f"{interpretation.domain_name} for which {self} holds.\n\n",
                f"In this case, "
                "\n\n",
            ])
        lines.extend([
            f"In particular, "


        ])

    def explain_evaluation(
        self, interpretation: Interpretation, input: NaryTuple, abbreviated=True
    ):
        resolved_input_tuple = input.get_resolved_terms(interpretation)
        short_explanation = " ".join(
            [
                f" {interpretation.name}({self}) =",
                f"{self.represent_extension()}",
                "\n\n",
                f"{resolved_input_tuple} ∈ {self.represent_extension()}",
                f"= {self(resolved_input_tuple, interpretation)}\n\n",
            ]
        )

        preamble = " ".join(
            [
                f"Object {input.represent_example_extension()}",
                f"satisfies {self}",
                f"in interpretation {interpretation.name}",
                f"iff {resolved_input_tuple}",
                f"is true in {interpretation.name}",
                f"[{input.represent_example_extension()}/{resolved_input_tuple}]",
                "\n\n",
                f"To evaluate predicate {self} with terms {input},",
                f"resolve terms under {interpretation.name}:\n",
                f"{input.represent_under_interpretation()} ⟼ {resolved_input_tuple}",
                "\n\n",
                f"Then, find {self}{resolved_input_tuple}",
                f"by determining if {resolved_input_tuple} ∈",
                f"{interpretation.name}({self}) =",
                f"the set of tuples from the domain of {interpretation.name} that",
                f"satisfy the predicate {str(self)[0]} under {interpretation.name}.",
                "\n\n",
            ]
        )
        if not abbreviated:
            return preamble + short_explanation
        return short_explanation
