import foundations
from punctilious.data.representations import \
    greek_alphabet_lowercase_serif_italic as _greek_alphabet_lowercase_serif_italic, \
    greek_alphabet_uppercase_serif_italic as _greek_alphabet_uppercase_serif_italic
from punctilious.data.connectors import operators_1 as _operators

preferences = foundations.get_preferences()
packages = foundations.get_packages()

greek_alphabet_lowercase_serif_italic = _greek_alphabet_lowercase_serif_italic.GreekAlphabetLowercaseSerifItalic()
print(greek_alphabet_lowercase_serif_italic.alpha.configurations[0])
print(greek_alphabet_lowercase_serif_italic.phi.configurations[1])
print(greek_alphabet_lowercase_serif_italic.psi.configurations[2])

greek_alphabet_uppercase_serif_italic = _greek_alphabet_uppercase_serif_italic.GreekAlphabetUppercaseSerifItalic()
print(greek_alphabet_uppercase_serif_italic.alpha.configurations[0])
print(greek_alphabet_uppercase_serif_italic.phi.configurations[1])
print(greek_alphabet_uppercase_serif_italic.psi.configurations[2])

operators: foundations.Package = _operators.Operators1Package()
# print(operators.conjunction.representation)
# print(operators.entailment.configurations[1])


# p = pathlib.Path('../punctilious_package_1/data/test/test_1.yaml')
# d = foundations.Package.instantiate_from_yaml_file(yaml_file_path=p)
# r = d.representations['conjunction']
# print(r.repr(args=('a', 'b'), encoding='unicode_extended'))
pass
