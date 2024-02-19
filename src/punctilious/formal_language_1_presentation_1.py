import typing
import log
import typesetting as ts
import formal_language_1 as fl1


class BinaryFormulaNotation:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name


class BinaryFormulaNotations:
    """A catalog of out-of-the-box binary_formula_notations."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(BinaryFormulaNotations, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._function_notation = BinaryFormulaNotation('function notation')
        self._infix_notation = BinaryFormulaNotation('infix notation')

    @property
    def function_notation(self) -> BinaryFormulaNotation:
        """The function notation."""
        return self._function_notation

    @property
    def infix_notation(self) -> BinaryFormulaNotation:
        """The infix notation."""
        return self._infix_notation


binary_formula_notations = BinaryFormulaNotations()


class BinaryFormulaNotationPreference(ts.Preference):
    def __init__(self, item: str, binary_formula_notation: BinaryFormulaNotation):
        super().__init__(item=item)
        self._binary_formula_notation: BinaryFormulaNotation = binary_formula_notation
        self._reset_value: BinaryFormulaNotation = binary_formula_notation

    @property
    def binary_formula_notation(self) -> BinaryFormulaNotation:
        return self._binary_formula_notation

    @binary_formula_notation.setter
    def binary_formula_notation(self, binary_formula_notation: BinaryFormulaNotation):
        self._binary_formula_notation = binary_formula_notation

    def reset(self) -> None:
        self.binary_formula_notation = self._reset_value


class Preferences:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_set: set[ts.Preference, ...] = set()
        super().__init__()
        section: str = "formal_language_1_presentation_1"
        self._binary_formula_notation = BinaryFormulaNotationPreference(item='binary formula notation',
                                                                        binary_formula_notation=binary_formula_notations.infix_notation)
        self._register(preference=self._binary_formula_notation)
        self._connective_symbol = ts.SymbolPreference(section=section, item="connective", attribute="symbol")
        self._register(preference=self._connective_symbol)

    def _register(self, preference: ts.Preference) -> None:
        self._internal_set.add(preference)

    @property
    def connective_symbol(self) -> ts.SymbolPreference:
        """binary formula notation preference"""
        return self._connective_symbol

    @property
    def binary_formula_notation(self) -> BinaryFormulaNotationPreference:
        """binary formula notation preference"""
        return self._binary_formula_notation

    def reset(self):
        for preference in self._internal_set:
            preference.reset()


preferences: Preferences = Preferences()


# Typesetting functions

def typeset_unary_formula_function_call(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)


def typeset_unary_formula_prefix_without_parenthesis(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[
    str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    if isinstance(o.term, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term, **kwargs)
    if isinstance(o.term, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    if isinstance(o.term_1, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term_1, **kwargs)
    if isinstance(o.term_1, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)
    yield from ts.typeset(o=ts.symbols.collection_separator, **kwargs)
    if isinstance(o.term_2, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term_2, **kwargs)
    if isinstance(o.term_2, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)


def typeset_binary_formula_infix(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    if isinstance(o.term_1, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term_1, **kwargs)
    if isinstance(o.term_1, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)
    yield from ts.typeset(o=ts.symbols.space, **kwargs)
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.space, **kwargs)
    if isinstance(o.term_2, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term_2, **kwargs)
    if isinstance(o.term_2, fl1.CompoundFormula):
        yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)


def load():
    # Representation: Symbolic Representation
    representation: ts.Representation = ts.representations.symbolic_representation

    # symbols
    ts.register_symbol(c=fl1.TypesettingClass.FL1_CONNECTIVE, symbol_preference=preferences.connective_symbol,
                       representation=representation)

    # formulas
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
                                   tc=fl1.TypesettingClass.FL1_BINARY_FORMULA, representation=representation)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call,
                                   tc=fl1.TypesettingClass.FL1_UNARY_FORMULA, representation=representation)

    # ts.register_typesetting_method(python_function=typeset_unary_formula_prefix_without_parenthesis,
    #                               tc=fl1.TypesettingClass.FL1_UNARY_FORMULA, representation=representation)

    # ts.register_typesetting_method(python_function=typeset_binary_formula_infix,
    #                               tc=fl1.TypesettingClass.FL1_BINARY_FORMULA, representation=representation)


load()
log.debug(f"Module {__name__}: loaded.")
