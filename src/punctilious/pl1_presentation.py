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
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = pl1.list_propositional_variables(o)
    yield from fl1_presentation.typeset_unary_formula_function_call(o=o,
        pl1_propositional_variables=pl1_propositional_variables, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula,
    pl1_propositional_variables: typing.Optional[tuple[pl1.PropositionalVariable]] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    if pl1_propositional_variables is None:
        pl1_propositional_variables: tuple[pl1.PropositionalVariable] = pl1.list_propositional_variables(o)
    yield from fl1_presentation.typeset_binary_formula_function_call(o=o,
        pl1_propositional_variables=pl1_propositional_variables, **kwargs)


def typeset_propositional_variable(o: pl1.PropositionalVariable, **kwargs) -> typing.Generator[str, None, None]:
    """PQR, else P1, P2, P3, ..."""
    pl1_propositional_variables: typing.Optional[dict[pl1.PropositionalVariable]] = None
    if "pl1_propositional_variables" in kwargs:
        pl1_propositional_variables: dict[pl1.PropositionalVariable] = kwargs["pl1_propositional_variables"]
    if pl1_propositional_variables is None:
        yield "P"
    else:
        yield pl1_propositional_variables[o]


def load():
    # Representation: Common Language
    # Flavor: Default
    # Language: EN-US
    treatment: ts.Treatment = fl1.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus
    ts.register_styledstring(tag=pl1.tags.conditional, text="material implication", treatment=treatment, flavor=flavor,
        language=language)
    ts.register_styledstring(tag=pl1.tags.negation, text="negation", treatment=treatment, flavor=flavor,
        language=language)

    # Representation: Common Language
    # Flavor: Default
    # Language: FR-CH
    treatment: ts.Treatment = fl1.treatments.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.frch
    ts.register_styledstring(tag=pl1.tags.conditional, text="conditionnel", treatment=treatment, flavor=flavor,
        language=language)
    ts.register_styledstring(tag=pl1.tags.negation, text="négation", treatment=treatment, flavor=flavor,
        language=language)

    # Representation: Symbolic Representation
    # Flavor: Default
    # Language: EN-US
    treatment: ts.Treatment = fl1.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus
    ts.register_symbol(tag=pl1.tags.conditional, symbol=ts.symbols.rightwards_arrow, treatment=treatment, flavor=flavor,
        language=language)
    ts.register_symbol(tag=pl1.tags.negation, symbol=ts.symbols.not_sign, treatment=treatment,
        flavor=pl1.flavors.connective_negation_not, language=language)
    ts.register_symbol(tag=pl1.tags.negation, symbol=ts.symbols.tilde, treatment=treatment,
        flavor=pl1.flavors.connective_negation_tilde, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
