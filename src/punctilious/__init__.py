import _util
from _util import get_yaml_from_package
import _identifiers
from _identifiers import create_uid, ensure_unique_identifier, ensure_slug, FlexibleSlug, FlexibleUUID, \
    load_unique_identifier, load_unique_identifiable, UniqueIdentifiable, UniqueIdentifier, Slug, SlugsDictionary
import _representation
from _representation import AbstractRepresentation, ensure_abstract_representations, ensure_abstract_representation, \
    latex_math, \
    load_abstract_representation, load_abstract_representations, \
    Tag, \
    TagsPreferences, \
    TagsAssignment, RendererForStringTemplate, \
    RendererForStringConstant, unicode_basic, unicode_extended
import _formal_language
from _formal_language import Connector, Connectors, declare_variable, ensure_formula, ensure_formula_arguments, \
    FormulaArguments, Formula
import _interpretation
from _interpretation import Interpreter
import _bundling
import formula_notations
import _greek_alphabet_lowercase_serif_italic
import _greek_alphabet_uppercase_serif_italic
import _latin_alphabet_lowercase_serif_italic
import _latin_alphabet_uppercase_serif_italic
# import _latin_alphabet_lowercase_serif_roman
import operators_1
import operators_1_representations
import operators_1_mappings

# import _propositional_logic_1
# import _tao_analysis_1_2006

prefs = _representation.TagsPreferences()
packages = _bundling.get_packages()

# formula_notations = _formula_notations.FormulaNotations()

greek_alphabet_lowercase_serif_italic = _greek_alphabet_lowercase_serif_italic.GreekAlphabetLowercaseSerifItalic()
greek_alphabet_uppercase_serif_italic = _greek_alphabet_uppercase_serif_italic.GreekAlphabetUppercaseSerifItalic()
latin_alphabet_lowercase_serif_italic = _latin_alphabet_lowercase_serif_italic.LatinAlphabetLowercaseSerifItalic()
latin_alphabet_uppercase_serif_italic = _latin_alphabet_uppercase_serif_italic.LatinAlphabetUppercaseSerifItalic()

# tao_analysis_1_2006 = _tao_analysis_1_2006.TaoAnalysis12006()
pass
