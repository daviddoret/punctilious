import typing

import fl1_presentation
import log
import typesetting as ts
import fl1
import pl1


def typeset_unary_formula_function_call(o: fl1.UnaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        l: pl1.PL1 = o.formal_language
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    yield from fl1_presentation.typeset_unary_formula_function_call(o=o, **kwargs)


def typeset_unary_formula_prefix_without_parenthesis(o: fl1.UnaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        l: pl1.PL1 = o.formal_language
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    yield from fl1_presentation.typeset_unary_formula_prefix_without_parenthesis(o=o, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        l: pl1.PL1 = o.formal_language
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    yield from fl1_presentation.typeset_binary_formula_function_call(o=o, **kwargs)


def typeset_binary_formula_infix(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        l: pl1.PL1 = o.formal_language
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = l.get_propositional_variable_tuple(phi=o)
        kwargs['pl1_propositional_variables'] = pl1_propositional_variables
    yield from fl1_presentation.typeset_binary_formula_infix(o=o, **kwargs)


def typeset_propositional_variable(o: pl1.PropositionalVariable,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        kwargs["representation"] = ts.representations.default
        yield from ts.typeset(o=ts.symbols.p_uppercase_serif_italic, **kwargs)
    else:
        if len(pl1_propositional_variables) < 4:
            index = pl1_propositional_variables.index(o)
            symbol: ts.Symbol = (ts.symbols.p_uppercase_serif_italic, ts.symbols.q_uppercase_serif_italic,
            ts.symbols.r_uppercase_serif_italic,)[index]
            kwargs["representation"] = ts.representations.default
            yield from ts.typeset(o=symbol, **kwargs)
        else:
            index = pl1_propositional_variables.index(o)
            kwargs["representation"] = ts.representations.default
            yield from ts.typeset(o=ts.IndexedSymbol(symbol=ts.symbols.p_uppercase_serif_italic, index=index + 1),
                **kwargs)


def load():
    # Representation: Common Language
    # Flavor: Default
    # Language: EN-US
    representation: ts.Representation = ts.representations.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus
    ts.register_styledstring(clazz=pl1.clazzes.conditional, text="material implication", representation=representation,
        flavor=flavor, language=language)
    ts.register_styledstring(clazz=pl1.clazzes.negation, text="negation", representation=representation, flavor=flavor,
        language=language)

    # Representation: Common Language
    # Flavor: Default
    # Language: FR-CH
    representation: ts.Representation = ts.representations.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.frch
    ts.register_styledstring(clazz=pl1.clazzes.conditional, text="conditionnel", representation=representation,
        flavor=flavor, language=language)
    ts.register_styledstring(clazz=pl1.clazzes.negation, text="négation", representation=representation, flavor=flavor,
        language=language)

    # Representation: Symbolic Representation
    # Flavor: Default
    # Language: EN-US
    representation: ts.Representation = ts.representations.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus
    ts.register_symbol(clazz=pl1.clazzes.conditional, symbol=ts.symbols.rightwards_arrow, representation=representation,
        flavor=flavor, language=language)
    ts.register_symbol(clazz=pl1.clazzes.negation, symbol=ts.symbols.not_sign, representation=representation,
        flavor=pl1.flavors.connective_negation_not, language=language)
    ts.register_symbol(clazz=pl1.clazzes.negation, symbol=ts.symbols.tilde, representation=representation,
        flavor=pl1.flavors.connective_negation_tilde, language=language)

    # Formulas
    flavor: ts.Flavor = fl1.flavors.formula_function_call
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
        clazz=pl1.clazzes.propositional_binary_formula, representation=representation, flavor=flavor, language=language)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call,
        clazz=pl1.clazzes.propositional_unary_formula, representation=representation, flavor=flavor, language=language)

    flavor: ts.Flavor = fl1.flavors.formula_prefix_no_parenthesis
    ts.register_typesetting_method(clazz=pl1.clazzes.propositional_unary_formula,
        python_function=typeset_unary_formula_prefix_without_parenthesis, representation=representation, flavor=flavor,
        language=language)
    flavor: ts.Flavor = fl1.flavors.formula_infix
    ts.register_typesetting_method(clazz=pl1.clazzes.propositional_binary_formula,
        python_function=typeset_binary_formula_infix, representation=representation, flavor=flavor, language=language)
    flavor: ts.Flavor = ts.flavors.default
    ts.register_typesetting_method(clazz=pl1.clazzes.propositional_variable,
        python_function=typeset_propositional_variable, representation=representation, flavor=flavor, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
