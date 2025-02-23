import typing

import punctilious_20250223.constants as const
import punctilious_20250223.pu_01_utilities as utilities
import punctilious_20250223.pu_02_unique_identifiers as identifiers
import punctilious_20250223.pu_03_representation as representation
import punctilious_20250223.options as options
import punctilious_20250223.pu_04_formal_language as formal_language
import punctilious_20250223.pu_06_meta_language as meta_language
import punctilious_20250223.pu_07_interpretation as interpretation

import punctilious_20250223.pu_11_bundling as _bundling
from punctilious_20250223.pu_11_bundling import load_abstract_representation, load_abstract_representations
import punctilious_20250223.pu_12_formula_notations as formula_notations

import punctilious_20250223.miscellaneous_1 as miscellaneous_1
import punctilious_20250223.pu_20_01_greek_alphabet_lowercase_serif_italic as greek_alphabet_lowercase_serif_italic
import punctilious_20250223.pu_20_02_greek_alphabet_uppercase_serif_italic as greek_alphabet_uppercase_serif_italic
import punctilious_20250223.pu_20_04_latin_alphabet_lowercase_serif_italic as latin_alphabet_lowercase_serif_italic
import punctilious_20250223.pu_20_05_latin_alphabet_uppercase_serif_italic as latin_alphabet_uppercase_serif_italic
import punctilious_20250223.pu_20_03_latin_alphabet_lowercase_serif_bold as latin_alphabet_lowercase_serif_bold
import punctilious_20250223.fonts as fonts

import punctilious_20250223.operators as operators
import punctilious_20250223.predicates as predicates
import punctilious_20250223.pu_20_06_constants_1 as constants_1

import punctilious_20250223.formal_language_mappings as formal_language_mappings

import punctilious_20250223.pu_13_default_interpreter as default_interpreter

from punctilious_20250223.declarations import declare_variable, declare_function

prefs = representation.Preferences()

# import _propositional_logic_1
import punctilious_20250223.tao_analysis_1_2006 as tao_analysis_1_2006

# packages = _bundling.get_packages()

utl = utilities
"""A shortcut for the `punctilious_20250223.utilities` module."""

ids = identifiers
"""A shortcut for the `punctilious_20250223.identifiers` module."""

rpr = representation
"""A shortcut for the `punctilious_20250223.representation` module."""

fml = formal_language
"""A shortcut for the `punctilious_20250223.formal_language` module."""

mtl = meta_language
"""A shortcut for the `punctilious_20250223.meta_language` module."""

# Implicit conversions
fml.configure_implicit_conversion(
    test_function=lambda formula: isinstance(formula, set),
    conversion_function=lambda formula: fml.Formula(mtl.unique_extension_tuple_connector, tuple(formula), ))
fml.configure_implicit_conversion(
    test_function=lambda formula: isinstance(formula, typing.Iterable),
    conversion_function=lambda formula: fml.Formula(mtl.extension_tuple_connector, tuple(formula), ))

pass
