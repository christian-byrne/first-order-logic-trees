from syntax.first_order_logic_syntax import AndExpr, ImpliesExpr, NotExpr, OrExpr, PredicateExpr, QuantifierExpr
from interpretation_function.constant import Constant
from modal_logic.interpretation import Interpretation


def evaluate(node, interpretation: Interpretation):
    if isinstance(node, PredicateExpr):
        # Base case: Evaluate the predicate with its terms
        predicate_obj = interpretation(node)
        return predicate_obj(node.terms, interpretation)

    elif isinstance(node, NotExpr):
        # Negation: recursively evaluate and negate the result
        return not evaluate(node.expr, interpretation)

    elif isinstance(node, AndExpr):
        # Conjunction: both left and right must be true
        return evaluate(node.left, interpretation) and evaluate(
            node.right, interpretation
        )

    elif isinstance(node, OrExpr):
        # Disjunction: either left or right (or both) must be true
        return evaluate(node.left, interpretation) or evaluate(
            node.right, interpretation
        )

    elif isinstance(node, ImpliesExpr):
        # Implication: equivalent to ¬left ∨ right
        return not evaluate(node.left, interpretation) or evaluate(
            node.right, interpretation
        )

    elif isinstance(node, QuantifierExpr):
        # Quantifiers: Handle both ∀ and ∃ quantifiers
        if node.quantifier == "∀":
            # Universal quantification: check for all objects in the domain
            for obj in interpretation.domain:
                # Temporarily bind the variable to the object
                interpretation.extend(Constant(node.variable), obj)
                if not evaluate(node.expr, interpretation):
                    interpretation.remove_constant_object_mapping(Constant(node.variable))
                    return False  # if any evaluation is False, ∀ fails
                interpretation.remove_constant_object_mapping(Constant(node.variable))
            return True  # all evaluations were True
        elif node.quantifier == "∃":
            # Existential quantification: check if any object in the domain satisfies
            for obj in interpretation.domain:
                interpretation.extend(Constant(node.variable), obj)
                if evaluate(node.expr, interpretation):
                    # Remove the temporary binding
                    interpretation.remove_constant_object_mapping(Constant(node.variable))
                    return True  # if any evaluation is True, ∃ succeeds
                interpretation.remove_constant_object_mapping(Constant(node.variable))
            return False  # none satisfied the expression
    else:
        raise ValueError(f"Unknown node type: {type(node)}")
