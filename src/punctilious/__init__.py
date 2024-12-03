import util
import presentation
import foundations
from punctilious.data.representations import \
    greek_alphabet_lowercase_serif_italic as _greek_alphabet_lowercase_serif_italic, \
    greek_alphabet_uppercase_serif_italic as _greek_alphabet_uppercase_serif_italic, \
    latin_alphabet_lowercase_serif_italic as _latin_alphabet_lowercase_serif_italic, \
    latin_alphabet_lowercase_serif_roman as _latin_alphabet_lowercase_serif_roman
from punctilious.data.connectors import operators_1 as _operators1
from punctilious.data.theorems import propositional_logic_1 as _propositional_logic1

prefs = presentation.TagsPreferences()
packages = foundations.get_packages()

greek_alphabet_lowercase_serif_italic = _greek_alphabet_lowercase_serif_italic.GreekAlphabetLowercaseSerifItalic()
print(greek_alphabet_lowercase_serif_italic.alpha.rep(prefs=prefs))
# print(greek_alphabet_lowercase_serif_italic.phi.configurations[1])
# print(greek_alphabet_lowercase_serif_italic.psi.configurations[2])

# greek_alphabet_uppercase_serif_italic = _greek_alphabet_uppercase_serif_italic.GreekAlphabetUppercaseSerifItalic()
# print(greek_alphabet_uppercase_serif_italic.alpha.configurations[0])
# print(greek_alphabet_uppercase_serif_italic.phi.configurations[1])
# print(greek_alphabet_uppercase_serif_italic.psi.configurations[2])

# latin_alphabet_lowercase_serif_italic = _latin_alphabet_lowercase_serif_italic.LatinAlphabetLowercaseSerifItalic()
# latin_alphabet_lowercase_serif_roman = _latin_alphabet_lowercase_serif_roman.LatinAlphabetLowercaseSerifRoman()

# operators_1 = _operators1.Operators1()
# print(operators_1.conjunction.representation.configurations[0])
# print(operators_1.entailment.representation.configurations[1])
# print(operators_1.entailment.representation.configurations[2])

# pl1 = _propositional_logic1.PropositionalLogic1()

pass
