import _formal_language
import _bundling

_constants_1 = _bundling.load_bundle_from_yaml_file_resource(path='data.connectors',
                                                             resource='constants_1.yaml')
_operators_1 = _bundling.load_bundle_from_yaml_file_resource(path='data.connectors',
                                                             resource='operators_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='data.representations',
                                              resource='constants_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='data.mappings',
                                              resource='constants_1.yaml')

successor: _formal_language.Connector = _operators_1.connectors.get_from_uuid(
    'f85163bf-381d-41fa-bdbb-70cd28bb826b', raise_error_if_not_found=True)

zero: _formal_language.Connector = _constants_1.connectors.get_from_uuid(
    '85927ea1-566e-4349-bab9-9845ba3a4b93', raise_error_if_not_found=True)
