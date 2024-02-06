import typing

import fl1_presentation
import log
import typesetting as ts
import fl1
import pl1


class Preferences:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._conditional_symbol = ts.SymbolPreference(name='conditional symbol', symbol=ts.symbols.rightwards_arrow)
        self._negation_symbol = ts.SymbolPreference(name='negation symbol', symbol=ts.symbols.not_sign)

    @property
    def conditional_symbol(self) -> ts.SymbolPreference:
        """The condition symbol preference setting."""
        return self._conditional_symbol

    @property
    def negation_symbol(self) -> ts.SymbolPreference:
        """The negation symbol preference setting."""
        return self._negation_symbol


preferences: Preferences = Preferences()


def typeset_unary_formula_function_call(o: fl1.UnaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[pl1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, pl1.PL1):
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    if pl1ml_meta_variables is None and isinstance(l, pl1.PL1ML):
        pl1ml_meta_variables: tuple[pl1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
        kwargs['pl1ml_meta_variables'] = pl1ml_meta_variables
    yield from fl1_presentation.typeset_unary_formula_function_call(o=o, **kwargs)


def typeset_unary_formula_prefix_without_parenthesis(o: fl1.UnaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[pl1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, pl1.PL1):
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    if pl1ml_meta_variables is None and isinstance(l, pl1.PL1ML):
        pl1ml_meta_variables: tuple[pl1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
        kwargs['pl1ml_meta_variables'] = pl1ml_meta_variables
    yield from fl1_presentation.typeset_unary_formula_prefix_without_parenthesis(o=o, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[pl1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, pl1.PL1):
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    if pl1ml_meta_variables is None and isinstance(l, pl1.PL1ML):
        pl1ml_meta_variables: tuple[pl1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
        kwargs['pl1ml_meta_variables'] = pl1ml_meta_variables
    yield from fl1_presentation.typeset_binary_formula_function_call(o=o, **kwargs)


def typeset_binary_formula_infix(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None,
    pl1ml_meta_variables: typing.Optional[tuple[pl1.MetaVariable]] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    l: fl1.FormalLanguage = o.formal_language
    if pl1_propositional_variables is None and isinstance(l, pl1.PL1):
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    if pl1ml_meta_variables is None and isinstance(l, pl1.PL1ML):
        pl1ml_meta_variables: tuple[pl1.MetaVariable] = l.get_meta_variable_tuple(phi=o)
        kwargs['pl1ml_meta_variables'] = pl1ml_meta_variables
    yield from fl1_presentation.typeset_binary_formula_infix(o=o, **kwargs)


def typeset_meta_variable(o: pl1.MetaVariable, pl1ml_meta_variables: typing.Optional[tuple[pl1.MetaVariable]] = None,
    **kwargs) -> typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1ml_meta_variables is None:
        kwargs["representation"] = ts.representations.technical_representation
        yield from ts.typeset(o=ts.symbols.p_uppercase_serif_italic_bold, **kwargs)
    else:
        if len(pl1ml_meta_variables) < 4:
            index = pl1ml_meta_variables.index(o)
            symbol: ts.Symbol = (ts.symbols.p_uppercase_serif_italic_bold, ts.symbols.q_uppercase_serif_italic_bold,
            ts.symbols.r_uppercase_serif_italic_bold,)[index]
            kwargs["representation"] = ts.representations.technical_representation
            yield from ts.typeset(o=symbol, **kwargs)
        else:
            index = pl1ml_meta_variables.index(o)
            kwargs["representation"] = ts.representations.technical_representation
            yield from ts.typeset(o=ts.IndexedSymbol(symbol=ts.symbols.p_uppercase_serif_italic_bold, index=index + 1),
                **kwargs)


def typeset_propositional_variable(o: pl1.PropositionalVariable,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        kwargs["representation"] = ts.representations.technical_representation
        yield from ts.typeset(o=ts.symbols.p_uppercase_serif_italic, **kwargs)
    else:
        if len(pl1_propositional_variables) < 4:
            index = pl1_propositional_variables.index(o)
            symbol: ts.Symbol = (ts.symbols.p_uppercase_serif_italic, ts.symbols.q_uppercase_serif_italic,
            ts.symbols.r_uppercase_serif_italic,)[index]
            kwargs["representation"] = ts.representations.technical_representation
            yield from ts.typeset(o=symbol, **kwargs)
        else:
            index = pl1_propositional_variables.index(o)
            kwargs["representation"] = ts.representations.technical_representation
            yield from ts.typeset(o=ts.IndexedSymbol(symbol=ts.symbols.p_uppercase_serif_italic, index=index + 1),
                **kwargs)


def load():
    # Representation: Symbolic Representation
    representation: ts.Representation = ts.representations.symbolic_representation
    ts.register_symbol(c=pl1.typesetting_classes.conditional, symbol_preference=preferences.conditional_symbol,
        representation=representation)
    ts.register_symbol(c=pl1.typesetting_classes.negation, symbol_preference=preferences.negation_symbol,
        representation=representation)

    # Formulas
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
        c=pl1.typesetting_classes.pl1_binary_formula, representation=representation)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call,
        c=pl1.typesetting_classes.pl1_unary_formula, representation=representation)

    ts.register_typesetting_method(c=pl1.typesetting_classes.pl1_unary_formula,
        python_function=typeset_unary_formula_prefix_without_parenthesis, representation=representation)
    ts.register_typesetting_method(c=pl1.typesetting_classes.pl1_binary_formula,
        python_function=typeset_binary_formula_infix, representation=representation)
    ts.register_typesetting_method(c=pl1.typesetting_classes.pl1_variable,
        python_function=typeset_propositional_variable, representation=representation)
    ts.register_typesetting_method(c=pl1.typesetting_classes.meta_variable, python_function=typeset_meta_variable,
        representation=representation)


load()
log.debug(f"Module {__name__}: loaded.")
