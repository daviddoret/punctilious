import log
import typesetting as ts


# Treatments

class Treatments:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Treatments, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._symbolic_representation = ts.Treatment(name="symbolic-representation")
        self._common_language = ts.Treatment(name="common-language")

    @property
    def common_language(self) -> ts.Treatment:
        """The common-language representation used in free text."""
        return self._common_language

    @property
    def symbolic_representation(self) -> ts.Treatment:
        """The formal representation used in formulas."""
        return self._symbolic_representation


treatments: Treatments = Treatments()


class Flavors:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Flavors, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        # formulas
        self._formula_function_call: ts.Flavor = ts.flavors.register(name="fl1.formula.function_call")
        self._formula_prefix_no_parenthesis: ts.Flavor = ts.flavors.register(name="fl1.formula.prefix_no_parenthesis",
            predecessor=self.formula_function_call)
        self._formula_infix: ts.Flavor = ts.flavors.register(name="fl1.formula.infix",
            predecessor=self._formula_function_call)

    @property
    def formula_function_call(self) -> ts.Flavor:
        """Typeset formulas with function notation, e.g.: f(x), g(x ,y), h(x ,y ,z), etc."""
        return self._formula_function_call

    @property
    def formula_prefix_no_parenthesis(self) -> ts.Flavor:
        """Typeset unary formulas with prefix notation and without parenthesis, e.g.: fx"""
        return self._formula_prefix_no_parenthesis

    @property
    def formula_infix(self) -> ts.Flavor:
        """Typeset binary formulas with infix notation, e.g.: x f y"""
        return self._formula_infix


flavors: Flavors = Flavors()


# TAGS

class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._formal_object = ts.tags.register(name="fl1.formal_object")
        self._connective = ts.tags.register(name="fl1.connective")
        self._fixed_arity_connective = ts.tags.register(name="fl1.fixed_arity_connective")
        self._variable_arity_connective = ts.tags.register(name="fl1.variable_arity_connective")
        self._binary_connective = ts.tags.register(name="fl1.binary_connective")
        self._unary_connective = ts.tags.register(name="fl1.unary_connective")
        self._compound_formula = ts.tags.register(name="fl1.compound_formula")
        self._fixed_arity_formula = ts.tags.register(name="fl1.fixed_arity_formula", predecessor=self._formal_object)
        self._binary_formula = ts.tags.register(name="fl1.binary_formula", predecessor=self._fixed_arity_formula)
        self._unary_formula = ts.tags.register(name="fl1.unary_formula", predecessor=self._fixed_arity_formula)
        self._compound_formula_class = ts.tags.register(name="fl1.compound_formula_class")
        self._connective_class = ts.tags.register(name="fl1.connective_class")
        self._formal_language = ts.tags.register(name="fl1.formal_language")
        self._formal_language_class = ts.tags.register(name="fl1.formal_language_class")
        self._meta_language = ts.tags.register(name="fl1.meta_language")
        self._ml1 = ts.tags.register(name="fl1.ml1")

    @property
    def binary_connective(self) -> ts.Tag:
        return self._binary_connective

    @property
    def binary_formula(self) -> ts.Tag:
        return (self._binary_formula)

    @property
    def compound_formula(self) -> ts.Tag:
        return self._compound_formula

    @property
    def compound_formula_class(self) -> ts.Tag:
        return self._compound_formula_class

    @property
    def connective(self) -> ts.Tag:
        return self._connective

    @property
    def connective_class(self) -> ts.Tag:
        return self._connective_class

    @property
    def fixed_arity_connective(self) -> ts.Tag:
        return self._fixed_arity_connective

    @property
    def fixed_arity_formula(self) -> ts.Tag:
        return self._fixed_arity_formula

    @property
    def formal_language(self) -> ts.Tag:
        return self._formal_language

    @property
    def formal_language_class(self) -> ts.Tag:
        return self._formal_language_class

    @property
    def formal_object(self) -> ts.Tag:
        return self._formal_object

    @property
    def meta_language(self) -> ts.Tag:
        return self._meta_language

    @property
    def ml1(self) -> ts.Tag:
        return self._ml1

    @property
    def unary_connective(self) -> ts.Tag:
        return self._unary_connective

    @property
    def unary_formula(self) -> ts.Tag:
        return self._unary_formula

    @property
    def variable_arity_connective(self) -> ts.Tag:
        return self._variable_arity_connective


tags = Tags()

log.debug(f"Module {__name__}: loaded.")
