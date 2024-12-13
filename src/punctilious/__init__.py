import _util
from _util import get_yaml_from_package
import _identifiers
from _identifiers import ensure_identifier, ensure_slug, FlexibleSlug, FlexibleUUID, Identifier, Slug, SlugsDictionary
import _presentation
from _presentation import Representation, ensure_representations, ensure_representation, latex_math, Tag, \
    TagsPreferences, \
    TagsAssignment, RendererForStringTemplate, \
    RendererForStringConstant, unicode_basic, unicode_extended
import _formal_language
from _formal_language import Connector, Connectors, declare_variable, ensure_formula, ensure_formula_arguments, \
    FormulaArguments, Formula
import _interpretation
from _interpretation import Interpreter
import _packaging
import _greek_alphabet_lowercase_serif_italic
import _greek_alphabet_uppercase_serif_italic
import _latin_alphabet_lowercase_serif_italic
import _latin_alphabet_uppercase_serif_italic
import _latin_alphabet_lowercase_serif_roman
import _formula_notations
import _operators_1
import _propositional_logic_1

prefs = _presentation.TagsPreferences()
packages = _packaging.get_packages()

greek_alphabet_lowercase_serif_italic = _greek_alphabet_lowercase_serif_italic.GreekAlphabetLowercaseSerifItalic()
greek_alphabet_uppercase_serif_italic = _greek_alphabet_uppercase_serif_italic.GreekAlphabetUppercaseSerifItalic()
latin_alphabet_uppercase_serif_italic = _latin_alphabet_uppercase_serif_italic.LatinAlphabetUppercaseSerifItalic()

formula_notations = _formula_notations.FormulaNotations()

operators_1 = _operators_1.Operators1()

# pl1 = _propositional_logic1.PropositionalLogic1()

pass
