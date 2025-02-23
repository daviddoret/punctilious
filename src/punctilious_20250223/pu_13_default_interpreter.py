"""A catalog of useful interpreters to parse mathematical formulas."""

import punctilious_20250223.pu_02_unique_identifiers as _uid
import punctilious_20250223.pu_03_representation as _rpr
import punctilious_20250223.pu_04_formal_language as _fml
import punctilious_20250223.pu_11_bundling as _bnd
import punctilious_20250223.pu_07_interpretation as _interpretation
import punctilious_20250223.pu_12_formula_notations as _formula_notations
import punctilious_20250223.options as _options
import punctilious_20250223.pu_20_06_constants_1 as constants_1
import punctilious_20250223.pu_20_01_greek_alphabet_lowercase_serif_italic as greek_alphabet_lowercase_serif_italic
import punctilious_20250223.pu_20_02_greek_alphabet_uppercase_serif_italic as greek_alphabet_uppercase_serif_italic
import punctilious_20250223.pu_20_04_latin_alphabet_lowercase_serif_italic as latin_alphabet_lowercase_serif_italic
import punctilious_20250223.pu_20_05_latin_alphabet_uppercase_serif_italic as latin_alphabet_uppercase_serif_italic
import punctilious_20250223.pu_20_03_latin_alphabet_lowercase_serif_bold as latin_alphabet_lowercase_serif_bold


def _generate_default_interpreter():
    prefs = _rpr.Preferences()
    prefs[_options.technical_language.unicode_basic] = 1
    prefs[_options.technical_language.unicode_extended] = 2
    prefs[_options.technical_language.latex_math] = _rpr.get_forbidden()

    operators_1_connectors = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.connectors',
                                                                      resource='operators.yaml')
    variables_1_connectors = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.connectors',
                                                                      resource='variables_1.yaml')
    constants_1_connectors = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.connectors',
                                                                      resource='constants_1.yaml')
    representations = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.representations',
                                                               resource='operators.yaml')
    mappings = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.mappings',
                                                        resource='operators.yaml')
    alpha2 = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.representations',
                                                      resource='latin_alphabet_uppercase_serif_italic.yaml')
    alpha1 = _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.representations',
                                                      resource='latin_alphabet_lowercase_serif_italic.yaml')
    _bnd.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.mappings',
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
    postfix_connectors = {}

    # Load variables from variables_1_connectors
    for connector in variables_1_connectors.connectors:
        connector: _fml.Connector
        if connector.formula_representation is _formula_notations.atomic_formula:
            rep = connector.connector_representation.rep(prefs=prefs)
            atomic_connectors[rep] = connector

    # Load operators from operators_1_connectors
    for connector in operators_1_connectors.connectors:
        connector: _fml.Connector
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

    # Load constants (atomic connectors) from constants_1_connectors
    for connector in constants_1_connectors.connectors:
        connector: _fml.Connector
        if connector.formula_representation is _formula_notations.atomic_formula:
            rep = connector.connector_representation.rep(prefs=prefs)
            atomic_connectors[rep] = connector

    interpreter = _interpretation.Interpret(
        uid=_uid.UniqueIdentifier(
            slug='default_interpreter',
            uuid='bda96859-9450-475c-a651-89d7dffcd2fe'),
        atomic_connectors=atomic_connectors,
        postfix_connectors=postfix_connectors,
        prefix_connectors=prefix_connectors,
        infix_connectors=infix_connectors,
        function_connectors=function_connectors)
    return interpreter


default_interpreter: _interpretation.Interpret = _generate_default_interpreter()

pass
