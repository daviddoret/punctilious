import typing
import log
import typesetting as ts
import fl1


# Typesetting functions

def typeset_unary_formula_function_call(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis)
    yield from ts.typeset(o=o.term, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis)


def typeset_unary_formula_prefix_without_parenthesis(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[
    str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=o.term, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis)
    yield from ts.typeset(o=o.term_1, **kwargs)
    yield from ts.typeset(o=ts.symbols.collection_separator)
    yield from ts.typeset(o=o.term_2, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis)


def typeset_binary_formula_infix(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.term_1, **kwargs)
    yield from ts.typeset(o=ts.symbols.space)
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.space)
    yield from ts.typeset(o=o.term_2, **kwargs)


def load():
    # Representation: Common Language
    # Flavor: Default
    # Language: EN-US
    treatment: ts.Treatment = fl1.treatments.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus

    ts.register_styledstring(clazz=fl1.clazzes.connective, text="connective", treatment=treatment, flavor=flavor,
        language=language)

    # Representation: Common Language
    # Flavor: Default
    # Language: FR-CH
    treatment: ts.Treatment = fl1.treatments.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.frch

    ts.register_styledstring(clazz=fl1.clazzes.connective, text="connecteur", treatment=treatment, flavor=flavor,
        language=language)

    # Representation: Symbolic Representation
    # Flavor: Default
    # Language: EN-US
    treatment: ts.Treatment = fl1.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus

    # symbols
    ts.register_symbol(clazz=fl1.clazzes.connective, symbol=ts.symbols.asterisk_operator, treatment=treatment,
        flavor=flavor, language=language)
    ts.register_symbol(clazz=fl1.clazzes.connective, symbol=ts.symbols.asterisk_operator, treatment=treatment,
        flavor=flavor, language=language)

    # formulas
    flavor: ts.Flavor = fl1.flavors.formula_function_call
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
        clazz=fl1.clazzes.binary_formula, treatment=treatment, flavor=flavor, language=language)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call, clazz=fl1.clazzes.unary_formula,
        treatment=treatment, flavor=flavor, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
