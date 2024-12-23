import punctilious._formal_language as _formal_language
import punctilious._bundling as _bundling

yaml_file_1 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                            resource='constants_1.yaml')
yaml_file_2 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                            resource='operators_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                              resource='tao_analysis_1_2006.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                              resource='tao_analysis_1_2006.yaml')
_theorems = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.theorems',
                                                          resource='tao_analysis_1_2006.yaml')

successor: _formal_language.Connector = yaml_file_2.connectors.get_from_uuid(
    'f85163bf-381d-41fa-bdbb-70cd28bb826b', raise_error_if_not_found=True)

zero: _formal_language.Connector = yaml_file_1.connectors.get_from_uuid(
    '85927ea1-566e-4349-bab9-9845ba3a4b93', raise_error_if_not_found=True)
