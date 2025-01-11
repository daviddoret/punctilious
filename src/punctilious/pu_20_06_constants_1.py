import punctilious.pu_02_identifiers as _ids
import punctilious.pu_04_formal_language as _fml
import punctilious.pu_11_bundling as _bnd

_constants_1 = _bnd.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                        resource='constants_1.yaml')
_bnd.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                         resource='constants_1.yaml')
_bnd.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                         resource='constants_1.yaml')

n: _fml.Connector = _fml.load_connector(
    '8cd28cf2-236b-40db-83e8-be83b888a029', raise_error_if_not_found=True)
"""The set of the natural numbers."""

zero: _fml.Connector = _fml.load_connector(
    '85927ea1-566e-4349-bab9-9845ba3a4b93', raise_error_if_not_found=True)
"""Zero."""
