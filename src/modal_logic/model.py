from contextlib import contextmanager

from modal_logic.domain import DomainOfDiscourse
from modal_logic.interpretation import Interpretation

from interpretation_function.variable import Variable


class Model:
    def __init__(self, name):
        self.name = name
        self.D = None
        self.I = None

    def with_interpretation_function(self, interpretation: Interpretation):
        self.I = interpretation
        if self.D and not self.I.domain:
            self.I.set_domain(self.D)
        return self

    def with_domain(self, domain: DomainOfDiscourse):
        self.D = domain
        self.D.model_name = self.name
        return self

    @contextmanager
    def bind_variable(self, var: Variable, domain_obj):
        if domain_obj not in self.D:
            msg = f"Attempted to bind {var} to {domain_obj} which is not in the domain."
            raise ValueError(msg)

        # Save the original binding of the variable if it exists
        original_binding = self.I.names.get(var, None)

        # Bind the variable to the object
        self.I.extend(var, domain_obj)

        try:
            yield
        finally:
            # Restore the original binding of the variable
            if original_binding is not None:
                self.I.extend(var, original_binding)
            else:
                self.I.restrict(var)

    def universal_instantiation(self, variable: Variable):
        for obj in self.D:
            with self.bind_variable(variable, obj):
                yield

    def existential_instantiation(self, variable: Variable, obj):
        with self.bind_variable(variable, obj):
            yield
