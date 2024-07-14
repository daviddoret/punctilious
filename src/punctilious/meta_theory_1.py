# import typing
import sys

import util_1 as u1
import presentation_layer_1 as pl1
from connectives_standard_library_1 import *

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')


# TODO: How to properly manage multiple output possibilities, e.g. phi() and lnot(phi())?
#   Should the inference rule list multiple conclusions, assuming disjunction?

def is_well_formed_formula_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tupl_OBSOLETE(t=p)
    a: as1.Tupl = as1.coerce_tupl_OBSOLETE(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    phi: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_formula(phi=phi):
        # Necessary case.
        phi: as1.Formula = is_well_formed_formula(phi)
        return phi
    else:
        # Impossible case.
        phi: as1.Formula = lnot(is_well_formed_formula(phi))
        return phi


def is_well_formed_inference_rule_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A python-function that is used as a a theory external-algorithm."""
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    i: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_inference_rule(i=i):
        i: as1.InferenceRule = as1.coerce_inference_rule(i=i)
        phi: as1.Formula = is_well_formed_inference_rule(t)
        return phi
    else:
        # This case is not possible because the punctilious framework forces the usage
        # of well-formed formulas.
        phi: as1.Formula = lnot(is_well_formed_inference_rule(t))
        return phi


def is_well_formed_theory_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tupl_OBSOLETE(t=p)
    a: as1.Tupl = as1.coerce_tupl_OBSOLETE(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    t: as1.Formula = as1.coerce_formula(phi=a[0])
    if as1.is_well_formed_theory(t=t):
        t: as1.Theory = as1.coerce_theory(t=t)
        phi: as1.Formula = is_well_formed_theory(t)
        return phi
    else:
        phi = lnot(is_well_formed_theory(t))
        return phi


with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    algo: as1.AlgorithmicTransformation = as1.AlgorithmicTransformation(
        a=is_well_formed_formula_algorithm,
        c=is_well_formed_formula(t),
        v=None,
        d={t, })
    mt1: as1.InferenceRule = as1.InferenceRule(
        t=algo,
        ref_ts=pl1.Monospace(text='MT1'))
    """The is-well-formed-formula algorithmic inference-rule.

    Abbreviation: MT1

    Variables: {t}

    Arguments: {t}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theory(t)
     - ¬(is-well-formed-theory(t))
    """

with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    algo: as1.AlgorithmicTransformation = as1.AlgorithmicTransformation(
        a=is_well_formed_inference_rule_algorithm,
        c=is_well_formed_inference_rule(t),
        v=None,
        d={t, })
    mt2: as1.InferenceRule = as1.InferenceRule(
        t=algo,
        ref_ts=pl1.Monospace(text='MT2'))
    """The is-well-formed-inference-rule algorithmic inference-rule.

    Abbreviation: MT2

    Variables: {t}

    Arguments: {t}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theory(t)
     - ¬(is-well-formed-theory(t))
    """

with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    algo: as1.AlgorithmicTransformation = as1.AlgorithmicTransformation(
        a=is_well_formed_theory_algorithm,
        c=is_well_formed_theory(t),
        v={t, },
        d={t, })
    mt3: as1.InferenceRule = as1.InferenceRule(
        t=algo,
        ref_ts=pl1.Monospace(text='MT3'))
    """The is-well-formed-theory algorithmic inference-rule.

    Abbreviation: MT3

    Variables: {t}

    Arguments: {t}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theory(t)
     - ¬(is-well-formed-theory(t))
    """

meta_theory_1 = as1.Axiomatization(d=(mt1, mt2, mt3,))

pass
