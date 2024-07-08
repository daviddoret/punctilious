# import typing
import sys

import util_1 as u1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
from connectives_standard_library_1 import *

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')


def is_well_formed_formula_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tupl(t=p)
    a: as1.Tupl = as1.coerce_tupl(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    phi: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_formula(phi=phi):
        phi: as1.Formula = is_well_formed_formula_predicate(phi)
        return phi
    else:
        # Impossible case.
        phi = lnot(is_well_formed_formula_predicate(phi))
        return phi


def is_well_formed_inference_rule_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tupl(t=p)
    a: as1.Tupl = as1.coerce_tupl(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    i: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_inference_rule(i=i):
        i: as1.InferenceRule = as1.coerce_inference_rule(i=i)
        phi: as1.Formula = is_well_formed_inference_rule_predicate(t)
        return phi
    else:
        # This case is not possible because the punctilious framework forces the usage
        # of well-formed formulas.
        phi = lnot(is_well_formed_inference_rule_predicate(t))
        return phi


def is_well_formed_theory_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tupl(t=p)
    a: as1.Tupl = as1.coerce_tupl(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    t: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_theory(t=t):
        t: as1.Theory = as1.coerce_theory(t=t)
        phi: as1.Formula = is_well_formed_theory_predicate(t)
        return phi
    else:
        phi = lnot(is_well_formed_theory_predicate(t))
        return phi


# Algorithms
def is_valid_statement_with_regard_to_theory_algorithm(p: as1.Tupl | None = None,
                                                       a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tupl(t=p)
    a: as1.Tupl = as1.coerce_tupl(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    t: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_theory(t=t):
        t = as1.coerce_theory(t=t)
        phi = theory_predicate(t)
        return phi
    else:
        phi = lnot(theory_predicate(t))
        return phi


with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    algo: as1.AlgorithmicTransformation = as1.AlgorithmicTransformation(
        external_algorithm=is_well_formed_theory_algorithm,
        c=is_well_formed_theory_predicate(t),
        v={t, },
        d={t, })
    mt1: as1.InferenceRule = as1.InferenceRule(
        t=algo,
        ref_ts=pl1.Monospace(text='MT1'))
    """The is-well-formed-theory algorithmic inference-rule.

    Abbreviation: MT1

    Variables: {t}

    Arguments: {t}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theory(t)
     - ¬(is-well-formed-theory(t))
    """

meta_theory_1 = as1.Axiomatization(d=(mt1,))

pass
