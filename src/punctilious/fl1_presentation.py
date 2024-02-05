import typing
import log
import typesetting as ts
import fl1


# Typesetting functions

def typeset_unary_formula_function_call(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)


def typeset_unary_formula_prefix_without_parenthesis(o: fl1.UnaryFormula, **kwargs) -> typing.Generator[
    str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=o.term, **kwargs)


def typeset_binary_formula_function_call(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.open_parenthesis, **kwargs)
    yield from ts.typeset(o=o.term_1, **kwargs)
    yield from ts.typeset(o=ts.symbols.collection_separator, **kwargs)
    yield from ts.typeset(o=o.term_2, **kwargs)
    yield from ts.typeset(o=ts.symbols.close_parenthesis, **kwargs)


def typeset_binary_formula_infix(o: fl1.BinaryFormula, **kwargs) -> typing.Generator[str, None, None]:
    yield from ts.typeset(o=o.term_1, **kwargs)
    yield from ts.typeset(o=ts.symbols.space, **kwargs)
    yield from ts.typeset(o=o.connective, **kwargs)
    yield from ts.typeset(o=ts.symbols.space, **kwargs)
    yield from ts.typeset(o=o.term_2, **kwargs)


def load():
    # Representation: Common Language
    # Preference: Default
    # Language: EN-US
    representation: ts.Representation = ts.representations.common_language
    preference: ts.Preference = ts.preferences.default
    language: ts.Language = ts.languages.enus

    ts.register_styledstring(hierarchical_class=fl1.hierarchical_classes.connective, text="connective",
        representation=representation)

    # Representation: Common Language
    # Preference: Default
    # Language: FR-CH
    representation: ts.Representation = ts.representations.common_language
    preference: ts.Preference = ts.preferences.default
    language: ts.Language = ts.languages.frch

    ts.register_styledstring(hierarchical_class=fl1.hierarchical_classes.connective, text="connecteur",
        representation=representation)

    # Representation: Symbolic Representation
    # Preference: Default
    # Language: EN-US
    representation: ts.Representation = ts.representations.symbolic_representation
    preference: ts.Preference = ts.preferences.default
    language: ts.Language = ts.languages.enus

    # symbols
    ts.register_symbol(c=fl1.hierarchical_classes.connective, symbol=ts.symbols.asterisk_operator,
        representation=representation)
    ts.register_symbol(c=fl1.hierarchical_classes.connective, symbol=ts.symbols.asterisk_operator,
        representation=representation)

    # formulas
    preference: ts.Preference = fl1.preferences.formula_function_call
    ts.register_typesetting_method(python_function=typeset_binary_formula_function_call,
        c=fl1.hierarchical_classes.binary_formula, representation=representation)
    ts.register_typesetting_method(python_function=typeset_unary_formula_function_call,
        c=fl1.hierarchical_classes.unary_formula, representation=representation)

    preference: ts.Preference = fl1.preferences.formula_prefix_no_parenthesis
    ts.register_typesetting_method(python_function=typeset_unary_formula_prefix_without_parenthesis,
        c=fl1.hierarchical_classes.unary_formula, representation=representation)

    preference: ts.Preference = fl1.preferences.formula_infix
    ts.register_typesetting_method(python_function=typeset_binary_formula_infix,
        c=fl1.hierarchical_classes.binary_formula, representation=representation)


load()
log.debug(f"Module {__name__}: loaded.")
