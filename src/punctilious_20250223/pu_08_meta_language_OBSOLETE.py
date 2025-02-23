"""The formal meta-language of the punctilious_20250223 package.

The meta-language module requires 1) formal-language and 2) interpretation.

"""

# special features
from __future__ import annotations

# external modules
import collections.abc
import typing
import yaml

# punctilious_20250223 modules
import punctilious_20250223.pu_02_unique_identifiers as _identifiers
import punctilious_20250223.pu_04_formal_language as _formal_language
import punctilious_20250223.pu_07_interpretation as _interpretation


def is_well_formed_tuple(phi: _formal_language.Formula) -> bool:
    """Determines whether a formula is a well-formed tuple.

    Global definition:
    A formula is a well-formed tuple if and only if its root connector is the tuple connector.

    Args:
        phi: a formula

    Returns:
        bool: True if the formula is a well-formed tuple, False otherwise.

    """
    phi = _formal_language.ensure_formula(o=phi)
    return phi.connector.is_connector_equivalent_to(_fundamental_connectors.extension_tuple_connector)


def is_well_formed_statement(phi: _formal_language.Formula) -> bool:
    """Determines whether a formula is a well-formed statement.

    Global definition:
    A formula is a well-formed statement if and only if it is of the form:
        `(V, P, c)`
    where:
     - `V` is a tuple of atomic formulas denoted as the variables of the statement,
     - `P` is a tuple of (supposedly predicate) formulas denoted as the premises of the statement, and
     - `c` is a (supposedly predicate) formula denoted as the conclusion of the statement.

    :param phi:
    :return:
    """

    # TODO: express_statement: implement the following ensure_X functions.
    # v = _meta_language.ensure_tuple_of_variables(o=v)
    # p = _meta_language.ensure_tuple_of_premises(o=p)
    # c = _meta_language.ensure_conclusion(o=c)

    phi = _formal_language.ensure_formula(o=phi)
    if not is_well_formed_tuple(phi=phi):
        return False
    elif arity(phi) != 3:
        return False
    else:
        # variables
        variables = phi.arguments[0]
        if not is_well_formed_tuple(phi=variables):
            return False
        elif not all(variable.is_atomic for variable in variables.arguments):
            # TODO: QUESTION: is_well_formed_statement: Is it correct / necessary to require that variables be atomic formulas?
            return False
        else:
            # premises
            premises = phi.arguments[1]
            if not is_well_formed_tuple(phi=premises):
                # TODO: is_well_formed_statement: is it necessary to verify that premises are propositions?
                return False
            else:
                # conclusion
                # TODO: is_well_formed_statement: is it necessary to verify that conclusion is a propositions?
                conclusion = phi.arguments[2]
                return True


def is_well_formed_derivation(phi: _formal_language.Formula, t: _formal_language.Formula) -> bool:
    """Determines whether a formula is a well-formed derivation.

    Global definition:
    A formula is a well-formed derivation if and only if it is of the form:
        `(S, M, P, c)`
    where:
     - `S` is a well-formed statement,
     - `M` is a tuple of formula pairs mapping statement variables to values denoted as the map of the derivation,
     - `P` is a tuple of (supposedly propositional) formulas denoted as the premises of the statement,
        where variables have been substituted with their values, and
     - `c` is a (supposedly propositional) formula denoted as the conclusion of the statement,
        where variables have been substituted with their values.

    :param phi:
    :return:
    """
    phi = _formal_language.ensure_formula(o=phi)
    # TODO: is_well_formed_derivation: implement function
    return True


def is_well_formed_axiom(phi: _formal_language.Formula) -> bool:
    """Determines whether a formula is a well-formed axiom.

    Global definition:
    TODO: is_well_formed_axiom: may any arbitrary formula be an axiom?
        or should axioms be restricted to certain forms? or to propositions?
        this looks like an important design choice. what is the best option?

    :param phi:
    :return:
    """
    phi = _formal_language.ensure_formula(o=phi)
    # TODO: is_well_formed_axiom: implement function
    return True


def is_well_formed_theory(phi: _formal_language.Formula) -> bool:
    """Determines whether a formula is a well-formed theory.

    Global definition:
    A formula is a well-formed theory if and only if it is of the form:
        `(A, D)`
    where:
     - `A` is a tuple of well-formed axioms, and
     - `D` is a tuple of well-formed derivations.

    :param phi:
    :return:
    """
    phi = _formal_language.ensure_formula(o=phi)
    # TODO: is_well_formed_theory: implement function
    return True


class Form:
    """A

    Examples:

    c1(...)

    c1(c2(...))

    c1()[arity=0]
    c1(...)[arity=1]
    c1(...)[arity=2]
    c1(...)[arity=n]

    [shape.s1]:=specification
    c3([shape=s1])

    """

    pass
