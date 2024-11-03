from typing import Any, Union

from interpretation_function.constant import Constant
from interpretation_function.variable import Variable
from interpretation_function.sentence_letter import SentenceLetter

from syntax.first_order_logic_syntax import PredicateExpr

from utils.config import Config
from utils.log import Logger

config = Config()
logger = Logger(__name__, config["log_level"])()


class Interpretation:
    """
    A comprehensive mapping that defines the semantics of all symbols within the
    logical language.

    In FOL, an interpretation (often denoted by 𝐼) is a structure that provides
    meaning to the symbols used in logical expressions, including constants,
    predicates, and function symbols.

    The interpretation assigns meanings to:
    1. Constants - Maps each constant to a specific object in the domain.
    2. Predicates - Maps each predicate to a set of tuples of domain elements for
       which the predicate holds true.
    3. Functions - Maps each function symbol to a function that takes domain
       elements as arguments and returns a domain element.
    """

    def __init__(self, name: str = "I", domain_name: str = "D", model_name: str = "M"):
        self.name = name
        self.domain_name = domain_name
        self.model_name = model_name
        self.domain = set()
        self.truth_values = {}
        self.names = {}
        self.predicates = {}

    def __str__(self):
        output = [f"Interpretation {self.name}"]

        # Format Domain
        domain_str = ", ".join(map(str, sorted(self.domain)))
        output.append(f"\nDomain:\n  {{ {domain_str} }}")

        # Format Constant Mappings
        if self.names:
            output.append("\nConstants ↦ Objects:")
            for constant, obj in sorted(self.names.items()):
                output.append(f"  {constant} ↦ {obj}")

        # Format Predicates and Extensions
        if self.predicates:
            output.append("\nPredicates and Extensions:")
            for predicate_name, predicate in self.predicates.items():
                if predicate.true_for:
                    extensions = predicate.represent_extension()
                else:
                    extensions = "∅"  # Empty set if no true arguments
                output.append(f"  {predicate_name} = {extensions}")

        # Format Sentence Letters and Truth Values
        if self.truth_values:
            output.append("\nSentence Letters Truth Values:")
            for sentence_letter, truth_value in sorted(
                self.truth_values.items(), key=lambda x: x[0].letter
            ):
                output.append(
                    f"  {sentence_letter}: {'True' if truth_value else 'False'}"
                )

        return "\n".join(output)

    def set_domain(self, domain):
        self.domain = domain
        return self

    def add_truth_value(self, sentence_letter: SentenceLetter, truth_value: bool):
        self.truth_values[sentence_letter] = truth_value
        return self

    def extend(self, constant: Union[Constant, Variable], obj: Any):
        logger.debug(f"Extending interpretation with {constant} ↦ {obj}")
        self.names[constant.name] = obj
        return self

    def restrict(self, constant: Union[Constant, Variable]):
        if constant.name not in self.names:
            if isinstance(constant, Variable):
                logger.warning(
                    f"Tried to unbind variable {constant} from interpretation but it was not found."
                )
            else:
                logger.warning(
                    f"Tried to remove {constant} from interpretation but it was not found."
                )
            return self
        del self.names[constant.name]
        return self

    def remove_constant_object_mapping(self, constant: Union[Constant, str]):
        for const in self.names:
            if const == constant:
                del self.names[str(const)]
                return self
        return self

    def add_predicate(self, predicate):
        self.predicates[predicate.name] = predicate
        return self

    # def get_domain_permutations(self, domain: List)

    def sentence_letter_truth_value(self, sentence_letter):
        return self.truth_values[sentence_letter]

    def __call__(
        self,
        symbol: Union[PredicateExpr, Constant, SentenceLetter, str],
    ):
        if isinstance(symbol, PredicateExpr):
            return self.predicates[symbol.name]
        if isinstance(symbol, Constant) or str(symbol) in self.names:
            return self.names[str(symbol)]
        if isinstance(symbol, Variable):
            if str(symbol) in self.names:
                return self.names[str(symbol)]
            else:
                return list(self.names.values())[0]
        if isinstance(symbol, SentenceLetter):
            return self.sentence_letter_truth_value(symbol.letter)
        if isinstance(symbol, str) and symbol in self.domain:
            return symbol
        else:
            error_msg = f"Expected a symbol but got {symbol} with type {type(symbol)}"
            raise TypeError(error_msg)
