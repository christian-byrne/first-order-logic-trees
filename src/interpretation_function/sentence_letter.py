class SentenceLetter:
    """
    A sentence letter is a propositional variable or atomic proposition that represents a whole statement with a truth value without involving predicates, functions, or quantifiers.

    Sentence letters are placeholders for simple true/false statements in FOL, as they are in propositional logic (TFL). They offer a way to directly assign truth values without needing predicates, names, or quantifiers, even within the more object-centered framework of FOL.


    """

    def __init__(self, letter: str, interpretation):
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
