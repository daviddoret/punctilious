import typing
import log
import typesetting as ts
import fl1_typesetting as fl1_ts
import fl1


def typeset_unary_formula_function_call(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis)
    yield from ts.typeset(o=o.term, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis)
    yield from ts.typeset(o=o.term_1, **kwargs)
    yield from ts.typeset(o=ts.symbols.collection_separator)
    yield from ts.typeset(o=o.term_2, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis)


def load():
    treatment: ts.Treatment = fl1_ts.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus

    # symbols
    ts.register_symbol(tag=fl1_ts.tags.connective, symbol=ts.symbols.asterisk_operator, treatment=treatment,
        flavor=flavor, language=language)
    ts.register_symbol(tag=fl1_ts.tags.connective, symbol=ts.symbols.asterisk_operator, treatment=treatment,
        flavor=flavor, language=language)

    # formulas
    flavor: ts.Flavor = fl1_ts.flavors.formula_function_call
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call, tag=fl1_ts.tags.binary_formula,
        treatment=treatment, flavor=flavor, language=language)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call, tag=fl1_ts.tags.unary_formula,
        treatment=treatment, flavor=flavor, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
