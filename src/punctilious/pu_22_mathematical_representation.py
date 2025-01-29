"""This module enriches the base representation layer with mathematical semantic."""

import re

import fontTools.cffLib

import punctilious.pu_03_representation as _rep
import punctilious.pu_04_formal_language as _fml


def convert_friendly_string_to_variable_name(friendly_string: str, font: _rep.Font):
    """Receives a string of the form `abc123` where:
     - `abc` is a series of one or more alphabetic ASCII characters,
     - `123` is a series of ASCII digit characters,
    and returns an AbstractRepresentation of a variable name of the form `abc_{123}`.

    :param friendly_string:
    :param font:
    :return:
    """
    # Regular expression pattern: ^([a-zA-Z])(\d*)$
    pattern = r'([a-zA-Z]+)(\d*)'
    match = re.fullmatch(pattern, friendly_string)
    if match:
        base: str = match.group(1)  # The first capture group (alphabetic character)
        if len(base) == 1:
            base_representation: _rep.AbstractRepresentation = font.get(base)
        else:
            base_representation: _rep.AbstractRepresentation = font.
        subscript: str = match.group(2)  # The second capture group (digits, or an empty string if none)
        return base, subscript
    else:
        raise ValueError("Input string does not match the expected format.")


def get_variable_abstract_representation(friendly_string: str) -> _rep.AbstractRepresentation:
    base, subscript = convert_friendly_string_to_variable_name(friendly_string, font=font)
    renderer_123 = _fml.RendererForStringConstant('123')
    subscript_123 = _fml.AbstractRepresentation(
        uid=None, renderers=(renderer_123,))
    x123 = pu.formal_language.Connector(
        connector_representation=pu.latin_alphabet_uppercase_serif_italic.x,
        subscript_representation=subscript_123,
        formula_representation=pu.formula_notations.atomic_formula,
    )
