import typing

import config
import log
import typesetting as ts
import formal_language_1 as fl1
import formal_language_1_presentation_1 as fl1p1
import propositional_logic_1 as lc1


class Preferences:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_set: typing.Union[set[None], set[ts.Preference, ...]] = set()
        super().__init__()
        section: str = "propositional_logic_1_presentation_1"
        self._conjunction_symbol = ts.SymbolPreference(name='conjunction symbol',
            symbol=ts.symbols[config.get_str(section=section, item="conjunction", attribute="symbol")])
        self._register(preference=self._conjunction_symbol)
        self._disjunction_symbol = ts.SymbolPreference(name='disjunction symbol',
            symbol=ts.symbols[config.get_str(section=section, item="conjunction", attribute="symbol")])
        self._register(preference=self._disjunction_symbol)
        self._material_implication_symbol = ts.SymbolPreference(name='material implication symbol',
            symbol=ts.symbols.material_conditional)
        self._register(preference=self._material_implication_symbol)
        self._negation_symbol = ts.SymbolPreference(name='negation symbol', symbol=ts.symbols.not_sign)
        self._register(preference=self._negation_symbol)

    def _register(self, preference: ts.Preference) -> None:
        self._internal_set.add(preference)

    @property
    def conjunction_symbol(self) -> ts.SymbolPreference:
        """The conjunction symbol preference setting."""
        return self._conjunction_symbol

    @property
    def disjunction_symbol(self) -> ts.SymbolPreference:
        """The disjunction symbol preference setting."""
        return self._disjunction_symbol

    @property
    def negation_symbol(self) -> ts.SymbolPreference:
        """The negation symbol preference setting."""
        return self._negation_symbol

    @property
    def material_implication_symbol(self) -> ts.SymbolPreference:
        """The condition symbol preference setting."""
        return self._material_implication_symbol

    @property
    def negation_symbol(self) -> ts.SymbolPreference:
        """The negation symbol preference setting."""
        return self._negation_symbol

    def reset(self):
        for preference in self._internal_set:
            preference.reset()


preferences: Preferences = Preferences()


def typeset_unary_formula_function_call(o: fl1.UnaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[lc1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[lc1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, lc1.PropositionalLogic) or isinstance(l, lc1.MetaLanguage):
        pl1_propositional_variables: tuple[lc1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
    if pl1ml_meta_variables is None and isinstance(l, lc1.MetaLanguage):
        pl1ml_meta_variables: tuple[lc1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
    yield from fl1p1.typeset_unary_formula_function_call(o=o, pl1_propositional_variables=pl1_propositional_variables,
        pl1ml_meta_variables=pl1ml_meta_variables, **kwargs)


def typeset_unary_formula_prefix_without_parenthesis(o: fl1.UnaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[lc1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[lc1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, lc1.PropositionalLogic) or isinstance(l, lc1.MetaLanguage):
        pl1_propositional_variables: tuple[lc1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
    if pl1ml_meta_variables is None and isinstance(l, lc1.MetaLanguage):
        pl1ml_meta_variables: tuple[lc1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
    yield from fl1p1.typeset_unary_formula_prefix_without_parenthesis(o=o,
        pl1_propositional_variables=pl1_propositional_variables, pl1ml_meta_variables=pl1ml_meta_variables, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[lc1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[lc1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, lc1.PropositionalLogic) or isinstance(l, lc1.MetaLanguage):
        pl1_propositional_variables: tuple[lc1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
    if pl1ml_meta_variables is None and isinstance(l, lc1.MetaLanguage):
        pl1ml_meta_variables: tuple[lc1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
    yield from fl1p1.typeset_binary_formula_function_call(o=o, pl1_propositional_variables=pl1_propositional_variables,
        pl1ml_meta_variables=pl1ml_meta_variables, **kwargs)


def typeset_binary_formula_infix(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[lc1.PropositionalVariable, ...]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[lc1.MetaVariable, ...]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, lc1.PropositionalLogic) or isinstance(l, lc1.MetaLanguage):
        pl1_propositional_variables: tuple[lc1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
    if pl1ml_meta_variables is None and isinstance(l, lc1.MetaLanguage):
        pl1ml_meta_variables: tuple[lc1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
    yield from fl1p1.typeset_binary_formula_infix(o=o, pl1_propositional_variables=pl1_propositional_variables,
        pl1ml_meta_variables=pl1ml_meta_variables, **kwargs)


def typeset_meta_variable(o: lc1.MetaVariable, pl1ml_meta_variables: typing.Optional[tuple[lc1.MetaVariable]] = None,
    representation: typing.Optional[ts.Representation] = None, **kwargs) -> typing.Generator[str, None, None]:
    """A, B, C, D, else A1, A2, A3, A4, A5, ..."""
    if pl1ml_meta_variables is None:
        representation = ts.representations.symbolic_representation
        yield from ts.typeset(o=ts.symbols.a_uppercase_serif_italic_bold, representation=representation, **kwargs)
    else:
        if len(pl1ml_meta_variables) < 5:
            index = pl1ml_meta_variables.index(o)
            symbol: ts.Symbol = (ts.symbols.a_uppercase_serif_italic_bold, ts.symbols.b_uppercase_serif_italic_bold,
            ts.symbols.c_uppercase_serif_italic_bold, ts.symbols.d_uppercase_serif_italic_bold,)[index]
            representation = ts.representations.symbolic_representation
            yield from ts.typeset(o=symbol, representation=representation, **kwargs)
        else:
            index = pl1ml_meta_variables.index(o) + 1
            representation = ts.representations.symbolic_representation
            yield from ts.typeset(o=ts.IndexedSymbol(symbol=ts.symbols.a_uppercase_serif_italic_bold, index=index),
                representation=representation, **kwargs)


def typeset_propositional_variable(o: lc1.PropositionalVariable,
    pl1_propositional_variables: typing.Optional[tuple[lc1.PropositionalVariable]] = None, **kwargs) -> \
typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        # A single propositional variable.
        kwargs2: dict = kwargs.copy()
        kwargs2['representation'] = ts.representations.symbolic_representation
        yield from ts.typeset(o=ts.symbols.p_uppercase_serif_italic, **kwargs2)
    else:
        if len(pl1_propositional_variables) < 4:
            index = pl1_propositional_variables.index(o)
            symbol: ts.Symbol = (ts.symbols.p_uppercase_serif_italic, ts.symbols.q_uppercase_serif_italic,
            ts.symbols.r_uppercase_serif_italic,)[index]
            kwargs2: dict = kwargs.copy()
            kwargs2['representation'] = ts.representations.symbolic_representation
            yield from ts.typeset(o=symbol, **kwargs2)
        else:
            index = pl1_propositional_variables.index(o)
            kwargs2: dict = kwargs.copy()
            kwargs2['representation'] = ts.representations.symbolic_representation
            yield from ts.typeset(o=ts.IndexedSymbol(symbol=ts.symbols.p_uppercase_serif_italic, index=index + 1),
                **kwargs2)


def load():
    # Representation: Symbolic Representation
    representation: ts.Representation = ts.representations.symbolic_representation
    ts.register_symbol(c=lc1.typesetting_classes.conjunction, symbol_preference=preferences.conjunction_symbol,
        representation=representation)
    ts.register_symbol(c=lc1.typesetting_classes.disjunction, symbol_preference=preferences.disjunction_symbol,
        representation=representation)
    ts.register_symbol(c=lc1.typesetting_classes.material_implication,
        symbol_preference=preferences.material_implication_symbol, representation=representation)
    ts.register_symbol(c=lc1.typesetting_classes.negation, symbol_preference=preferences.negation_symbol,
        representation=representation)

    # Formulas
    # ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
    #    c=lc1.typesetting_classes.pl1_binary_formula, representation=representation)
    # ts.register_typesetting_method(python_function=typeset_unary_formula_function_call,
    #    c=lc1.typesetting_classes.pl1_unary_formula, representation=representation)

    ts.register_typesetting_method(c=lc1.typesetting_classes.pl1_unary_formula,
        python_function=typeset_unary_formula_prefix_without_parenthesis, representation=representation)
    ts.register_typesetting_method(c=lc1.typesetting_classes.pl1_binary_formula,
        python_function=typeset_binary_formula_infix, representation=representation)
    ts.register_typesetting_method(c=lc1.typesetting_classes.pl1_variable,
        python_function=typeset_propositional_variable, representation=representation)
    ts.register_typesetting_method(c=lc1.typesetting_classes.meta_variable, python_function=typeset_meta_variable,
        representation=representation)


load()
log.debug(f"Module {__name__}: loaded.")
