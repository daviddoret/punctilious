import punctilious._formal_language as _formal_language
import punctilious._bundling as _bundling

_constants_1 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                             resource='constants_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                              resource='constants_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                              resource='constants_1.yaml')

n: _formal_language.Connector = _constants_1.connectors.get_from_uuid(
    '8cd28cf2-236b-40db-83e8-be83b888a029', raise_error_if_not_found=True)
"""The set of the natural numbers."""

zero: _formal_language.Connector = _constants_1.connectors.get_from_uuid(
    '85927ea1-566e-4349-bab9-9845ba3a4b93', raise_error_if_not_found=True)
"""Zero."""
