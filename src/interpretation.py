from typing import Any, List, Union


class SentenceLetter:
    """
    A sentence letter is a propositional variable or atomic proposition that represents a whole statement with a truth value without involving predicates, functions, or quantifiers.

    Sentence letters are placeholders for simple true/false statements in FOL, as they are in propositional logic (TFL). They offer a way to directly assign truth values without needing predicates, names, or quantifiers, even within the more object-centered framework of FOL.


    """

    def __init__(self, letter: str, interpretation: "Interpretation"):
        self.letter = letter
        self.included_in_interpretations = [interpretation]

    def __str__(self):
        return self.letter

    def add_to_interpretation(self, interpretation):
        self.included_in_interpretations.append(interpretation)
        return self

    def __eq__(self, other):
        for interpretation in self.included_in_interpretations:
            if other in interpretation.truth_values:
                if (
                    interpretation.truth_values[other]
                    != interpretation.truth_values[self.letter]
                ):
                    return False
        return True


class Predicate:
    """
    A predicate is a function that takes objects as arguments and returns a truth value. In FOL, predicates are used to describe properties or relationships between objects in the domain. Predicates can have multiple arguments, and the truth value of the predicate is determined by the objects assigned to these arguments in the interpretation.

    """

    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity
        self.true_for = set()

    def __str__(self):
        return self.name

    def extend(self, objects):
        if isinstance(objects, (list, tuple, set)):
            self.true_for.update(tuple(objects))
        elif isinstance(objects, str):
            self.true_for.add(objects)
        else:
            raise ValueError(
                f"Predicate {self.name} expects a string or list of strings as arguments."
            )
        return self

    def __getitem__(self, objects):
        if len(objects) != self.arity:
            raise ValueError(
                f"Predicate {self.name} expects {self.arity} arguments, but {len(objects)} were provided."
            )
        self.true_for.add(objects)

    def __call__(self, objects):
        return objects in self.true_for


class Constant:
    """
    A constant is a symbol that represents a specific object in the domain. In FOL, constants are used to refer to specific individuals, objects, or entities within the domain. Each constant is assigned a unique name or label that identifies the object it represents.

    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: Union["Constant", str]):
        if isinstance(other, Constant):
            return self.name == other.name
        return self.name == other


class Function:
    """
    A function is a mapping from a set of input values (arguments) to an output value. In FOL, functions are used to represent relationships between objects in the domain that produce a new object as a result of applying the function to the input objects. Functions can have multiple arguments and return a single object as the result of the function application.

    """

    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity
        self.mapping = {}

    def __str__(self):
        return self.name

    # def __getitem__(self, objects):
    #   if len(objects) != self.arity:
    #     raise ValueError(f"Function {self.name} expects {self.arity} arguments, but {len(objects)} were provided.")
    #   return self.mapping[objects]

    # def __setitem__(self, objects, result):
    #   if len(objects) != self.arity:
    #     raise ValueError(f"Function {self.name} expects {self.arity} arguments, but {len(objects)} were provided.")
    #   self.mapping[objects] = result

    # def __call__(self, objects):
    #   return self.mapping[objects]


Symbol = Union[Constant, Predicate, Function, SentenceLetter]


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

    def __init__(self, name: str = "I"):
        self.name = name
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
            output.append("\nConstants and Object Mappings:")
            for constant, obj in sorted(self.names.items()):
                output.append(f"  {constant} ↦ {obj}")

        # Format Predicates and Extensions
        if self.predicates:
            output.append("\nPredicates and Extensions:")
            for predicate_name, predicate in sorted(self.predicates.items()):
                if predicate.true_for:
                    print(predicate.true_for)
                    extensions = ", ".join(
                        f"{args}" for args in sorted(predicate.true_for)
                    )
                else:
                    extensions = "∅"  # Empty set if no true arguments
                output.append(f"  {predicate_name} = {{ {extensions} }}")

        # Format Sentence Letters and Truth Values
        if self.truth_values:
            output.append("\nSentence Letters and Truth Values:")
            for sentence_letter, truth_value in sorted(
                self.truth_values.items(), key=lambda x: x[0].letter
            ):
                output.append(
                    f"  {sentence_letter}: {'True' if truth_value else 'False'}"
                )

        return "\n".join(output)

    def add_to_domain(self, obj: Union[str, List[str]]):
        if isinstance(obj, (list, tuple, set)):
            self.domain.update(obj)
        else:
            self.domain.add(obj)
        return self

    def add_truth_value(self, sentence_letter: SentenceLetter, truth_value: bool):
        self.truth_values[sentence_letter] = truth_value
        return self

    def add_constant_object_mapping(self, constant: Constant, obj: Any):
        self.names[constant.name] = obj
        return self

    def remove_constant_object_mapping(self, constant: Union[Constant, str]):
        for const in self.names:
            if const == constant:
                del self.names[str(const)]
                return self
        return self

    def add_predicate(self, predicate: Predicate):
        self.predicates[predicate.name] = predicate
        return self

    def sentence_letter_truth_value(self, sentence_letter):
        return self.truth_values[sentence_letter]

    def __call__(self, symbol: Symbol):
        if isinstance(symbol, SentenceLetter):
            return self.sentence_letter_truth_value(symbol.letter)
        if isinstance(symbol, Constant):
            return self.names[symbol.name]
        if isinstance(symbol, Predicate):
            return symbol.true_for
        if isinstance(symbol, str):
            # See if a predicate has same name
            if symbol in self.predicates:
                return self.predicates[symbol]

        return symbol
