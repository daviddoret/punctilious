import pu_01_utilities as _utilities
import pu_02_identifiers as _identifiers
import pu_03_representation as _representation
import pu_04_formal_language as _formal_language
import pu_05_foundational_connectors as _fundamental_connectors
import pu_07_interpretation as _interpretation
import pu_08_meta_language as _meta_language


def express_statement(v, p, c):
    """Expresses a statement in the formal language.

    Args:
        v: a tuple of variables
        p: a tuple of premises
        c: a conclusion
    """
    # TODO: express_statement: implement the following ensure_X functions.
    # v = _meta_language.ensure_tuple_of_variables(o=v)
    # p = _meta_language.ensure_tuple_of_premises(o=p)
    # c = _meta_language.ensure_conclusion(o=c)
    return _formal_language.Formula(c=_fundamental_connectors.tuple1, a=(v, p, c,))


def is_valid_derivation(d, t):
    """

    :param d:
    :param t:
    :return:
    """
    _meta_language.is_well_formed_derivation(phi=d, raise_error_if_false=True)
    _meta_language.is_well_formed_theory(phi=t, raise_error_if_false=True)
    # IMPLEMENT VALIDATION HERE
    invoked_derivation_rule = d.rule
    if not invoked_derivation_rule in t.derivation_rules:
        return False
    if not all(is_valid(d=premise, t=t) for premise in d.premises):
        return False
    pass


def derive(d, t):
    """Given a theory `t`, and a derivation `d`,
     validates that `d` is a valid derivation in `t`,
     and return a new theory `t'` with `d` appended to its derivations.

    Args:
        d: a derivation
        t: a theory
    """
    # TODO: derive: Implement the following validation functions.
    # d = _meta_language.ensure_derivation(o=d)
    # t = _meta_language.ensure_theory(o=t)
    if not is_derivation_in_theory(d=d, t=t):
        raise ValueError('The derivation is not in the theory.')
    return _meta_language.Theory(d=(*t.derivations, d), )
