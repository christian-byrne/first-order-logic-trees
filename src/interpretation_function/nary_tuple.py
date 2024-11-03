from typing import TypeVar, Generic, Collection


from interpretation_function.constant import Constant

T = TypeVar("T")


class NaryTuple(Generic[T]):
    def __init__(self, terms: Collection[T]):
        if not terms:
            self.terms = []  # Empty tuple
        elif isinstance(terms, NaryTuple):
            self.terms = terms.terms
        elif not isinstance(terms, Collection):
            raise ValueError(f"Expected a collection but got {terms}")
        else:
            self.terms = list(terms)

    def represent_under_interpretation(self, interpretation_name="I") -> str:
        as_codomain = [f"{interpretation_name}({item})" for item in self.terms]
        return f"({', '.join(as_codomain)})"

    def represent_example_extension(self) -> str:
        alphabet = "defghijklmnopqrstuvwxyzabc"
        letters = [alphabet[i] for i in range(len(self.terms))]
        return f"({','.join(letters)})"

    def get_resolved_terms(self, interpretation):
        """
        Return the version of self in which any constants have been replaced by their
        corresponding objects in the interpretation's domain.
        """
        resolved = []
        for term in self.terms:
            if isinstance(term, Constant):
                resolved.append(interpretation(term))
            else:
                resolved.append(term)
        return NaryTuple(resolved)

    def __iter__(self):
        return iter(self.terms)

    def __getitem__(self, key):
        return self.terms[key]

    def __len__(self):
        return len(self.terms)

    def __eq__(self, other: "NaryTuple"):
        if not isinstance(other, NaryTuple):
            raise TypeError(f"Expected Tuple but got {type(other)}")
        return len(set(self.terms).difference(other.terms)) == 0

    def __str__(self):
        if len(self.terms) > 2:
            return f"(...{', ...'.join(map(str, self.terms[:3]))}...)"
        return f"({', '.join(map(str, self.terms))})"
