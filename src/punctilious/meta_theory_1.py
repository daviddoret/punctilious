# import typing
import sys

import constants_1 as c1
import util_1 as u1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
import connectives_standard_library_1 as csl1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')


# TODO: How to properly manage multiple output possibilities, e.g. phi() and lnot(phi())?
#   Should the inference rule list multiple conclusions, assuming disjunction?

def is_well_formed_formula(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    a0: as1.Formula = a[0]
    phi: as1.Formula = as1.coerce_formula(phi=a0)
    if as1.is_well_formed_formula(phi=phi):
        # Necessary case.
        phi: as1.Formula = csl1.is_well_formed_formula(phi)
        return phi
    else:
        # Technically impossible case.
        raise u1.ApplicativeError(
            msg='The argument `a0` is not a well-formed formula. '
                'It follows that the statement :math:`\text{is-well-formed-formula}(a_{0})` cannot be derived.',
            code=c1.ERROR_CODE_MT1_003,
            a0=a0
        )


def is_well_formed_inference_rule(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A python-function that is used as a theory external-algorithm."""
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    a0: as1.Formula = a[0]
    i: as1.Formula = as1.coerce_formula(phi=a0)
    if as1.is_well_formed_inference_rule(i=i):
        as1.coerce_inference_rule(i=i)
        phi: as1.Formula = csl1.is_well_formed_inference_rule(t)
        return phi
    else:
        raise u1.ApplicativeError(
            msg='The argument `a0` is not a well-formed inference-rule. '
                'It follows that the statement :math:`\text{is-well-formed-inference-rule}(a_{0})` cannot be derived.',
            code=c1.ERROR_CODE_MT1_001,
            a0=a0
        )


def is_well_formed_theory(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A python-function used as a theory external algorithm."""
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    a0: as1.Formula = a[0]
    t1: as1.Formula = as1.coerce_formula(phi=a0)
    if as1.is_well_formed_theory(t=t1):
        t2: as1.Theory = as1.coerce_theory(t=t1)
        phi: as1.Formula = csl1.is_well_formed_theory(t2)
        return phi
    else:
        raise u1.ApplicativeError(
            msg='The argument `a0` is not a well-formed theory. '
                'It follows that the statement :math:`\text{is-well-formed-theory}(a_{0})` cannot be derived.',
            code=c1.ERROR_CODE_MT1_002,
            a0=a0
        )


def is_compatible_with_is_well_formed_formula(phi: as1.FlexibleFormula) -> bool:
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_1 = csl1.is_well_formed_formula(x)
        test_1, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_1, psi=phi, variables={x, })
        if test_1:
            return True
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_2 = csl1.lnot(csl1.is_well_formed_formula(x))
        test_2, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_2, psi=phi, variables={x, })
        if test_2:
            return True
        else:
            return False


def is_compatible_with_is_well_formed_inference_rule(phi: as1.FlexibleFormula) -> bool:
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_1 = csl1.is_well_formed_inference_rule(x)
        test_1, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_1, psi=phi, variables={x, })
        if test_1:
            return True
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_2 = csl1.lnot(csl1.is_well_formed_inference_rule(x))
        test_2, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_2, psi=phi, variables={x, })
        if test_2:
            return True
        else:
            return False


def is_compatible_with_is_well_formed_theory(phi: as1.FlexibleFormula) -> bool:
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_1 = csl1.is_well_formed_theory(x)
        test_1, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_1, psi=phi, variables={x, })
        if test_1:
            return True
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_2 = csl1.lnot(csl1.is_well_formed_theory(x))
        test_2, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_2, psi=phi, variables={x, })
        if test_2:
            return True
        else:
            return False


with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    algo: as1.AlgorithmicTransformation = as1.AlgorithmicTransformation(
        a=is_well_formed_formula,
        i=is_compatible_with_is_well_formed_formula,
        c=csl1.is_well_formed_formula(t),
        v=None,
        d={t, })
    mt1: as1.InferenceRule = as1.InferenceRule(
        f=algo,
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
        a=is_well_formed_inference_rule,
        i=is_compatible_with_is_well_formed_inference_rule,
        c=csl1.is_well_formed_inference_rule(t),
        v=None,
        d={t, })
    mt2: as1.InferenceRule = as1.InferenceRule(
        f=algo,
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
        a=is_well_formed_theory,
        i=is_compatible_with_is_well_formed_theory,
        c=csl1.is_well_formed_theory(t),
        v={t, },
        d={t, })
    mt3: as1.InferenceRule = as1.InferenceRule(
        f=algo,
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
