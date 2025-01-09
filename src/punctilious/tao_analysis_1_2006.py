import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_07_interpretation as _interpretation
import punctilious.pu_11_bundling as _bundling
import punctilious.pu_12_formula_notations as _formula_notations

import punctilious.options as _options

yaml_file_1 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                            resource='constants_1.yaml')
yaml_file_2 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                            resource='operators_1.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                              resource='tao_analysis_1_2006.yaml')
_bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                              resource='tao_analysis_1_2006.yaml')


def _configure_tao_interpreter():
    global _tao_interpreter
    if _tao_interpreter is not None:
        pass
    else:
        prefs = _representation.Preferences()
        prefs[_options.technical_language.unicode_basic] = 1
        prefs[_options.technical_language.unicode_extended] = 2
        prefs[_options.technical_language.latex_math] = _representation.get_forbidden()

        # representations = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
        #                                                                resource='tao_analysis_1_2006.yaml')
        mappings = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                                                 resource='tao_analysis_1_2006.yaml')

        # TODO: NICE_TO_HAVE: When building the interpreter, read programmatically the mappings,
        #   to populate the tokens, to prevent a situation where some representations are enriched
        #   in memory, leading to inconsistencies in the interpretation.

        # generate infix connectors
        atomic_connectors = {}
        infix_connectors = {}
        function_connectors = {}
        prefix_connectors = {}
        postfix_connectors = {}

        # Load variables from variables_1_connectors
        for connector in mappings.connectors:
            connector: _formal_language.Connector
            if connector.formula_representation is _formula_notations.atomic_formula:
                rep = connector.connector_representation.rep(prefs=prefs)
                atomic_connectors[rep] = connector
            elif connector.formula_representation is _formula_notations.infix_formula:
                rep = connector.connector_representation.rep(prefs=prefs)
                infix_connectors[rep] = connector
            elif connector.formula_representation is _formula_notations.function_formula:
                rep = connector.connector_representation.rep(prefs=prefs)
                function_connectors[rep] = connector
            elif connector.formula_representation is _formula_notations.prefix_formula:
                rep = connector.connector_representation.rep(prefs=prefs)
                prefix_connectors[rep] = connector
            elif connector.formula_representation is _formula_notations.postfix_formula:
                rep = connector.connector_representation.rep(prefs=prefs)
                postfix_connectors[rep] = connector

        interpreter = _interpretation.Interpret(
            uid=_identifiers.UniqueIdentifier(
                slug='tao_analysis_1_2006_interpreter',
                uuid='12af7828-364d-4943-b9ea-92553d35566e'),
            atomic_connectors=atomic_connectors,
            postfix_connectors=postfix_connectors,
            prefix_connectors=prefix_connectors,
            infix_connectors=infix_connectors,
            function_connectors=function_connectors)
        _tao_interpreter = interpreter


_tao_interpreter: _interpretation.Interpret | None = None

_configure_tao_interpreter()
test = _identifiers.load_unique_identifiable(
    o={'uid': {'slug': 'tao_analysis_1_2006_interpreter', 'uuid': '12af7828-364d-4943-b9ea-92553d35566e'}})
_statements = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.statements',
                                                            resource='tao_analysis_1_2006.yaml')

successor: _formal_language.Connector = _identifiers.load_unique_identifiable(
    'f85163bf-381d-41fa-bdbb-70cd28bb826b', raise_error_if_not_found=True)

zero: _formal_language.Connector = _identifiers.load_unique_identifiable(
    '85927ea1-566e-4349-bab9-9845ba3a4b93', raise_error_if_not_found=True)
