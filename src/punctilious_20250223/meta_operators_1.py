"""A catalog of meta operators.

The connectors declared in this YAML file are also hard-coded in the punctilious_20250223.formal_language.
"""

import punctilious_20250223.pu_04_formal_language as _formal_language
import punctilious_20250223.pu_11_bundling as _bundling

_meta_operators_1 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.connectors',
                                                                  resource='meta_operators_1.yaml')

statement: _formal_language.Connector = _meta_operators_1.connectors.get_from_uuid(
    'c138b200-111a-4a40-ac3c-c8afa8e615fb', raise_error_if_not_found=True)
"""The `statement` meta operator is an axiom, a theorem, or an hypothesis.
"""

variables: _formal_language.Connector = _meta_operators_1.connectors.get_from_uuid(
    '0489e6f7-022e-48a4-82bf-dcb5907653b7', raise_error_if_not_found=True)
"""The `variables` meta operator is used to declare the variables in a statement.
"""

premises: _formal_language.Connector = _meta_operators_1.connectors.get_from_uuid(
    'b78ed901-37d2-4a97-a7a8-588b69dab20a', raise_error_if_not_found=True)
"""The `premises` meta operator is used to declare the premises in a statement.
"""

conclusion: _formal_language.Connector = _meta_operators_1.connectors.get_from_uuid(
    'd66e41ae-9989-48b5-986e-31db0995661d', raise_error_if_not_found=True)
"""The `conclusion` meta operator is used to declare the conclusion in a statement.
"""
