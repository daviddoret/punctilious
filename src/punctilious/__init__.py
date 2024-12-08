import _util
from _util import get_yaml_from_package
import _presentation
from _presentation import Representation, ensure_representations, ensure_representation, latex_math, Tag, \
    TagsPreferences, \
    TagsAssignment, RendererForStringTemplate, \
    RendererForStringConstant, unicode_basic, unicode_extended
import _foundations
from _foundations import FormulaArguments, Formula, ensure_formula, ensure_formula_arguments, Connector, Connectors
import _interpretation
from _interpretation import Interpreter
import _greek_alphabet_lowercase_serif_italic
import _greek_alphabet_uppercase_serif_italic
import _latin_alphabet_lowercase_serif_italic
import _latin_alphabet_uppercase_serif_italic
import _latin_alphabet_lowercase_serif_roman
import _operators_1 as _operators1
import _propositional_logic_1

prefs = _presentation.TagsPreferences()
packages = _foundations.get_packages()

greek_alphabet_lowercase_serif_italic = _greek_alphabet_lowercase_serif_italic.GreekAlphabetLowercaseSerifItalic()
greek_alphabet_uppercase_serif_italic = _greek_alphabet_uppercase_serif_italic.GreekAlphabetUppercaseSerifItalic()
latin_alphabet_uppercase_serif_italic = _latin_alphabet_uppercase_serif_italic.LatinAlphabetUppercaseSerifItalic()
# operators_1 = _operators1.Operators1()

# pl1 = _propositional_logic1.PropositionalLogic1()

pass
