import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_10_bundling as _bundling

_variables_1 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                             resource='variables_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                              resource='latin_alphabet_lowercase_serif_italic.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                              resource='latin_alphabet_uppercase_serif_italic.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                              resource='variables_1.yaml')

proposition_1: _formal_language.Connector = _variables_1.connectors.get_from_uuid(
    'faac89cf-2d37-4ea9-8055-4e382bf82e4d', raise_error_if_not_found=True)
"""A propositional variable."""

proposition_2: _formal_language.Connector = _variables_1.connectors.get_from_uuid(
    '07826bfd-865d-442b-b658-30b44aeb79af', raise_error_if_not_found=True)
"""A propositional variable."""

proposition_3: _formal_language.Connector = _variables_1.connectors.get_from_uuid(
    'd3b59b31-f698-4481-936f-3d329c651782', raise_error_if_not_found=True)
"""A propositional variable."""

p = proposition_1
q = proposition_2
r = proposition_3

number_1: _formal_language.Connector = _variables_1.connectors.get_from_uuid('78c97ee4-bb26-45a8-8503-ca239e4e0ede',
                                                                             raise_error_if_not_found=True)
number_2: _formal_language.Connector = _variables_1.connectors.get_from_uuid('6dcfe458-7d9d-4a2a-947f-abd000946a0a',
                                                                             raise_error_if_not_found=True)
number_3: _formal_language.Connector = _variables_1.connectors.get_from_uuid('52106c5e-a149-4267-b908-f169a256de47',
                                                                             raise_error_if_not_found=True)

x = number_1
y = number_2
z = number_3
