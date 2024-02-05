import typing

import fl1_presentation
import log
import typesetting as ts
import fl1
import pl1


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
    # Representation: Common Language
    # Preference: Default
    # Language: EN-US
    representation: ts.Representation = ts.representations.symbolic_representation
    preference: ts.Preference = ts.preferences.default
    language: ts.Language = ts.languages.enus
    ts.register_styledstring(clazz=pl1.clazzes.conditional, text="material implication", representation=representation,
        preference=preference, language=language)
    ts.register_styledstring(clazz=pl1.clazzes.negation, text="negation", representation=representation,
        preference=preference, language=language)

    # Representation: Common Language
    # Preference: Default
    # Language: FR-CH
    representation: ts.Representation = ts.representations.common_language
    preference: ts.Preference = ts.preferences.default
    language: ts.Language = ts.languages.frch
    ts.register_styledstring(clazz=pl1.clazzes.conditional, text="conditionnel", representation=representation,
        preference=preference, language=language)
    ts.register_styledstring(clazz=pl1.clazzes.negation, text="négation", representation=representation,
        preference=preference, language=language)

    # Representation: Symbolic Representation
    # Preference: Default
    # Language: EN-US
    representation: ts.Representation = ts.representations.symbolic_representation
    preference: ts.Preference = ts.preferences.default
    language: ts.Language = ts.languages.enus
    ts.register_symbol(clazz=pl1.clazzes.conditional, symbol=ts.symbols.rightwards_arrow, representation=representation,
        preference=preference, language=language)
    ts.register_symbol(clazz=pl1.clazzes.negation, symbol=ts.symbols.not_sign, representation=representation,
        preference=pl1.preferences.connective_negation_not, language=language)
    ts.register_symbol(clazz=pl1.clazzes.negation, symbol=ts.symbols.tilde, representation=representation,
        preference=pl1.preferences.connective_negation_tilde, language=language)

    # Formulas
    preference: ts.Preference = fl1.preferences.formula_function_call
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
        clazz=pl1.clazzes.propositional_binary_formula, representation=representation, preference=preference,
        language=language)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call,
        clazz=pl1.clazzes.propositional_unary_formula, representation=representation, preference=preference,
        language=language)

    preference: ts.Preference = fl1.preferences.formula_prefix_no_parenthesis
    ts.register_typesetting_method(clazz=pl1.clazzes.propositional_unary_formula,
        python_function=typeset_unary_formula_prefix_without_parenthesis, representation=representation,
        preference=preference, language=language)
    preference: ts.Preference = fl1.preferences.formula_infix
    ts.register_typesetting_method(clazz=pl1.clazzes.propositional_binary_formula,
        python_function=typeset_binary_formula_infix, representation=representation, preference=preference,
        language=language)
    preference: ts.Preference = ts.preferences.default
    ts.register_typesetting_method(clazz=pl1.clazzes.propositional_variable,
        python_function=typeset_propositional_variable, representation=representation, preference=preference,
        language=language)
    ts.register_typesetting_method(clazz=pl1.clazzes.meta_variable, python_function=typeset_meta_variable,
        representation=representation, preference=preference, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
