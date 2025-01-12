"""This module provides a catalog of abstract representations for various formula notations.

"""
import punctilious.pu_02_unique_identifiers as _uid
import punctilious.pu_03_representation as _rpr
import punctilious.pu_11_bundling as _bnd

_formula_notations = _bnd.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                                              resource='formula_notations.yaml')

atomic_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'f6bd05d7-ee5b-4480-9d59-ea9fa3a13516',
    raise_error_if_not_found=True)
"""A formula representation for atomic formulas of the form: `𝗖` where 𝗖 is the connector.
"""

function_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'cd1df2f9-f04d-4321-8430-5191082da985',
    raise_error_if_not_found=True)
"""A formula representation for function formulas of the form: `𝗖(𝗮₁, 𝗮₂, …, 𝗮ₙ)` where 𝗖 is the connector and 𝗮ᵢ
is an argument.
"""

infix_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation('d83bd1a4-97cf-4a7e-975d-21711333b971',
                                                                               raise_error_if_not_found=True)
"""A formula representation for infix formulas of the form: `𝗮₁ 𝗖 𝗮₂` where 𝗖 is the connector and 𝗮ᵢ
is an argument.
"""

prefix_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation('ca64ae2f-f8a7-4a87-a99d-57d86a8ba0ad',
                                                                                raise_error_if_not_found=True)
"""A formula representation for prefix formulas of the form: `𝗖𝗮₁` where 𝗖 is the connector and 𝗮ᵢ
is an argument.
"""

postfix_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation('af99c47e-c6b8-43e0-a8f4-6331ba79e8fd',
                                                                                 raise_error_if_not_found=True)
"""A formula representation for postfix formulas of the form: `𝗮₁𝗖` where 𝗖 is the connector and 𝗮ᵢ
is an argument.
"""

system_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation('8df8b738-3efc-4da5-928a-ea4d7d053598',
                                                                                raise_error_if_not_found=True)
"""A formula representation for system formulas of the form: `(𝗖, (𝗮₁, 𝗮₂, …, 𝗮ₙ))` where 𝗖 is the connector
and 𝗮ᵢ is an argument.
"""

parenthesized_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '2d050cf8-bb21-4af3-879f-2faf34b35722',
    raise_error_if_not_found=True)
"""A formula representation for parenthesized formulas of the form: `(𝗮₁, 𝗮₂, …, 𝗮ₙ)` where 𝗮ᵢ is an argument.
This notation introduces some ambiguity because the connector is not explicitly represented.
"""

angle_bracketed_formula: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '2d050cf8-bb21-4af3-879f-2faf34b35722',
    raise_error_if_not_found=True)
"""A formula representation for angle-bracketed formulas of the form: `⟨𝗮₁, 𝗮₂, …, 𝗮ₙ⟩` where 𝗮ᵢ is an argument.
This notation introduces some ambiguity because the connector is not explicitly represented.
"""
