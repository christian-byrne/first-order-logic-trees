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
