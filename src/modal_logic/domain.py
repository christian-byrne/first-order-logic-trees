from typing import TypeVar, Generic, Union, List, Collection, Any

from utils.config import Config
from utils.log import Logger

from utils.text_convert.to_latex import t, im, mm, st, symb, symb_sub
from utils.text_convert.to_markdown import df, h

from semantics.definitions import definition

config = Config()
logger = Logger(__name__, config["log_level"])()

T = TypeVar("T")


class DomainOfDiscourse(Generic[T]):
    """
    Represents the domain of discourse for an interpretation.

    The domain of discourse is the set of objects over which the quantifiers in a
    logical language range. It is a set of objects that are relevant to the
    interpretation of the logical language.

    The domain of discourse is typically denoted by a capital letter such as D.
    """

    def __init__(self, name: str = "D", model_name: str = "M"):
        logger.info(h(f"Creating Domain {im(name)}", 2))
        logger.info(df("domain", definition("domain")))
        self.name = name
        self.model_name = model_name
        self.domain = set()

    def __str__(self):
        return f"{self.name}"

    def __contains__(self, item: T):
        logger.info(h(f"Checking if {im(item)} is in Domain {im(self.name)}", 5))
        result = item in self.domain

        symbol = symb("is in") if result else symb("is not in")
        logger.info(
            f"{symb_sub('semantically entails', self.model_name)} {im(item)} {symbol} {im(self.name)}"
        )
        return result

    def represent_domain(self):
        return "{" + ", ".join(map(str, sorted(self.domain))) + "}"

    def expand(self, obj: Union[T, List[T]]):
        logger.info(h(f"Expanding Domain {im(self.name)}", 3))
        logger.info(df("domain expansion", definition("domain expansion")))

        logger.info(h("Domain Before Expansion", 4))
        logger.info(f"{im(self.name)} = {st(self.domain)}")

        if isinstance(obj, Collection) and len(obj) > 0:
            self.domain.update(obj)
        else:
            self.domain.add(obj)

        logger.info(h("Domain After Expansion", 4))
        logger.info(f"{im(self.name)}' = {st(self.domain)}")

        return self

    def restrict(self, obj: Union[T, List[T]]):
        if isinstance(obj, (list, tuple, set)):
            self.domain.difference_update(obj)
        else:
            self.domain.remove(obj)
        return self

    def __iter__(self):
        return iter(self.domain)

    def __len__(self):
        return len(self.domain)

    def __eq__(self, other):
        if not isinstance(other, DomainOfDiscourse):
            msg = f"Cannot compare DomainOfDiscourse with {type(other)} object."
            logger.error(msg)
            raise TypeError(msg)

        logger.info(h(f"Comparing Domains {im(self.name)} and {im(other.name)}", 4))
        logger.info(df("set equality", definition("set equality")))

        logger.info(h("Domain 1", 5))
        logger.info(f"{im(self.name)} = {st(self.domain)}")

        logger.info(h("Domain 2", 5))
        logger.info(f"{im(other.name)} = {st(other.domain)}")

        logger.info(h("Equality Check", 5))

        # Formal definition of set equality
        result = self.domain.issubset(other.domain) and other.domain.issubset(
            self.domain
        )

        sem_entail = symb_sub("semantically entails", self.model_name)
        not_sem_entail = symb_sub("not semantically entails", self.model_name)

        symbol = sem_entail if self.domain.issubset(other.domain) else not_sem_entail
        logger.info(f"{symbol} {st(self.domain)} {symb('subset')} {st(other.domain)}")

        symbol = sem_entail if other.domain.issubset(self.domain) else not_sem_entail
        logger.info(f"{symbol} {st(other.domain)} {symb('subset')} {st(self.domain)}")

        symbol = sem_entail if result else not_sem_entail
        logger.info(f"{symbol} {st(self.domain)} = {st(other.domain)}")

        return result

    def __ne__(self, other):
        return not self.__eq__(other)
