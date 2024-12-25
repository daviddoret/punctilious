"""A catalog of useful interpreters to parse mathematical formulas."""

import punctilious.representation as _representation
import punctilious.formal_language as _formal_language
import punctilious._bundling as _bundling
import punctilious.interpretation as _interpretation
import punctilious.options as _options
import punctilious.formula_notations as _formula_notations
import punctilious.latin_alphabet_lowercase_serif_italic as _latin_alphabet_lowercase_serif_italic
import punctilious.latin_alphabet_uppercase_serif_italic as _latin_alphabet_uppercase_serif_italic


def generate_interpreter():
    prefs = _representation.Preferences()
    prefs[_options.technical_language.unicode_basic] = 1
    prefs[_options.technical_language.unicode_extended] = 2
    prefs[_options.technical_language.latex_math] = _representation.get_forbidden()

    operators_1_connectors = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                                           resource='operators_1.yaml')
    variables_1_connectors = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                                           resource='variables_1.yaml')
    constants_1_connectors = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                                           resource='constants_1.yaml')
    representations = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                                                    resource='operators_1.yaml')
    mappings = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                                             resource='operators_1.yaml')
    alpha2 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                                           resource='latin_alphabet_uppercase_serif_italic.yaml')
    alpha1 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                                           resource='latin_alphabet_lowercase_serif_italic.yaml')
    _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                                  resource='variables_1.yaml')

    # TODO: NICE_TO_HAVE: When building the interpreter, read programmatically the mappings,
    #   to populate the tokens, to prevent a situation where some representations are enriched
    #   in memory, leading to inconsistencies in the interpretation.

    # generate infix connectors
    # variable_connectors = {}
    atomic_connectors = {}
    infix_connectors = {}
    function_connectors = {}
    prefix_connectors = {}

    # Load variables from variables_1_connectors
    for connector in variables_1_connectors.connectors:
        connector: _formal_language.Connector
        if connector.formula_representation is _formula_notations.atomic_formula:
            rep = connector.connector_representation.rep(prefs=prefs)
            atomic_connectors[rep] = connector

    # Load operators from operators_1_connectors
    for connector in operators_1_connectors.connectors:
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

    # Load constants (atomic connectors) from constants_1_connectors
    for connector in constants_1_connectors.connectors:
        connector: _formal_language.Connector
        if connector.formula_representation is _formula_notations.atomic_formula:
            rep = connector.connector_representation.rep(prefs=prefs)
            atomic_connectors[rep] = connector

    interpreter = _interpretation.Interpreter(
        # variable_connectors=variable_connectors,
        atomic_connectors=atomic_connectors,
        prefix_connectors=prefix_connectors,
        infix_connectors=infix_connectors,
        function_connectors=function_connectors)
    return interpreter


generate_interpreter()
pass
