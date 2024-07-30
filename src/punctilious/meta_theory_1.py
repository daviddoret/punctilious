import typing
import sys

import constants_1 as c1
import util_1 as u1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')


# TODO: How to properly manage multiple output possibilities, e.g. phi() and lnot(phi())?
#   Should the inference rule list multiple conclusions, assuming disjunction?

class IsWellFormedTheoryAlgorithm(as1.TransformationByExternalAlgorithm):

    def data_validation(self,
                        p: as1.FlexibleTupl | None = None,
                        a: as1.FlexibleTupl | None = None,
                        m: as1.FlexibleMap | None = None) -> bool:
        p = as1.coerce_tuple(t=p, interpret_none_as_empty=False, canonic_conversion=False)
        a = as1.coerce_tuple(t=p, interpret_none_as_empty=False, canonic_conversion=False)
        m = as1.coerce_map(m=m, interpret_none_as_empty=False)
        if p.arity != 0:
            raise u1.ApplicativeError(msg='wrong arity')
        if a.arity != 1:
            raise u1.ApplicativeError(msg='wrong arity')
        # Retrieve the arguments
        t: as1.Theory = as1.coerce_theory(t=a[0], interpret_none_as_empty=False, canonical_conversion=False)
        pass

    def execute_algorithm(self,
                          p: as1.FlexibleTupl | None = None,
                          a: as1.FlexibleTupl | None = None,
                          m: as1.FlexibleMap | None = None) -> [bool, as1.Formula]:
        p = as1.coerce_tuple(t=p, interpret_none_as_empty=False, canonic_conversion=False)
        a = as1.coerce_tuple(t=p, interpret_none_as_empty=False, canonic_conversion=False)
        m = as1.coerce_map(m=m, interpret_none_as_empty=False)
        pass


def is_well_formed_formula_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A"""
    p: as1.Tupl = as1.coerce_tuple(t=p, interpret_none_as_empty=True)
    a: as1.Tupl = as1.coerce_tuple(t=a, interpret_none_as_empty=True)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    a0: as1.Formula = a[0]
    phi: as1.Formula = as1.coerce_formula(phi=a0)
    if as1.is_well_formed_formula(phi=phi):
        # Necessary case.
        phi: as1.Formula = as1.is_well_formed_formula_connective(phi)
        return phi
    else:
        # Technically impossible case.
        raise u1.ApplicativeError(
            msg='The argument `a0` is not a well-formed formula. '
                'It follows that the statement :math:`\text{is-well-formed-formula}(a_{0})` cannot be derived.',
            code=c1.ERROR_CODE_MT1_003,
            a0=a0
        )


def is_well_formed_inference_rule_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A python-function that is used as a theory external-algorithm."""
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    a0: as1.Formula = a[0]
    i: as1.Formula = as1.coerce_formula(phi=a0)
    if as1.is_well_formed_inference_rule(i=i):
        as1.coerce_inference_rule(i=i)
        phi: as1.Formula = as1.is_well_formed_inference_rule_connective(t)
        return phi
    else:
        raise u1.ApplicativeError(
            msg='The argument `a0` is not a well-formed inference-rule. '
                'It follows that the statement :math:`\text{is-well-formed-inference-rule}(a_{0})` cannot be derived.',
            code=c1.ERROR_CODE_MT1_001,
            a0=a0
        )


def is_well_formed_theory_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """A python-function used as a theory external algorithm.

    :param p: Premises.
    :param a: Complementary arguments.
    :return:
    """
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 1:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    a0: as1.Formula = a[0]
    t1: as1.Formula = as1.coerce_formula(phi=a0)
    if as1.is_well_formed_theory(t=t1):
        t2: as1.Theory = as1.coerce_theory(t=t1)
        phi: as1.Formula = as1.is_well_formed_theory_connective(t2)
        return phi
    else:
        raise u1.ApplicativeError(
            msg='The argument `a[0]` is not a well-formed theory. '
                'It follows that the statement :math:`\\text{is-well-formed-theory}(a_{0})` cannot be derived.',
            code=c1.ERROR_CODE_MT1_002,
            a0=a0,
            a=a,
            p=p
        )


def is_compatible_with_is_well_formed_formula(phi: as1.FlexibleFormula) -> bool:
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_1 = as1.is_well_formed_formula_connective(x)
        test_1, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_1, psi=phi, variables={x, })
        if test_1:
            return True
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_2 = as1.logical_negation_connective(as1.is_well_formed_formula_connective(x))
        test_2, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_2, psi=phi, variables={x, })
        if test_2:
            return True
        else:
            return False


def is_compatible_with_is_well_formed_inference_rule(phi: as1.FlexibleFormula) -> bool:
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_1 = as1.is_well_formed_inference_rule_connective(x)
        test_1, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_1, psi=phi, variables={x, })
        if test_1:
            return True
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_2 = as1.logical_negation_connective(as1.is_well_formed_inference_rule_connective(x))
        test_2, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_2, psi=phi, variables={x, })
        if test_2:
            return True
        else:
            return False


def is_compatible_with_is_well_formed_theory_algorithm(phi: as1.FlexibleFormula) -> bool:
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_1 = as1.is_well_formed_theory_connective(x)
        test_1, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_1, psi=phi, variables={x, })
        if test_1:
            return True
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        solution_2 = as1.logical_negation_connective(as1.is_well_formed_theory_connective(x))
        test_2, _ = as1.is_formula_equivalent_with_variables_2(phi=solution_2, psi=phi, variables={x, })
        if test_2:
            return True
        else:
            return False


with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    algo: as1.TransformationByExternalAlgorithm = as1.TransformationByExternalAlgorithm(
        algo=is_well_formed_formula_algorithm,
        check=is_compatible_with_is_well_formed_formula,
        o=as1.is_well_formed_formula_connective(t),
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
    algo: as1.TransformationByExternalAlgorithm = as1.TransformationByExternalAlgorithm(
        algo=is_well_formed_inference_rule_algorithm,
        check=is_compatible_with_is_well_formed_inference_rule,
        o=as1.is_well_formed_inference_rule_connective(t),
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

# INFERENCE-RULE: MT3: is-well-formed-theory
with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as t:
    _mt3: as1.TransformationByExternalAlgorithm = as1.let_x_be_a_transformation_by_external_algorithm(
        algo=is_well_formed_theory_algorithm,
        check=None,  # is_compatible_with_is_well_formed_theory
        o=as1.is_well_formed_theory_connective(t),
        i=None,
        v={t, },
        d={t, })
    mt3: as1.InferenceRule = as1.InferenceRule(
        f=_mt3,
        ref_ts=pl1.Monospace(text='MT3'))
    """The is-well-formed-theory algorithmic inference-rule.

    Abbreviation: MT3

    Variables: {t}

    Arguments: {t}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theory(t)
    """

# INFERENCE-RULE: ⊥1: inconsistency-1: P and ¬P
with as1.let_x_be_a_variable(formula_ts='T') as t, as1.let_x_be_a_variable(formula_ts='P') as p:
    inconsistency_1: as1.InferenceRule = as1.InferenceRule(
        f=as1.let_x_be_a_transformation_by_variable_substitution(
            i=(
                as1.is_well_formed_theory_connective(t),
                t | as1.proves_connective | p,
                t | as1.proves_connective | as1.logical_negation_connective(p)),
            o=as1.is_inconsistent_connective(t),
            v={p, t, }),
        ref_ts=pl1.Monospace(text='⊥1'))
    """The inconsistency-1 inference rule: P and ¬P

    Abbreviation: ⊥1

    Premises:
     1. is-a-well-formed-theory(T)
     2. T ⊢ P
     3. T ⊢ ¬P 

    Conclusion: T ⊢ ⊥

    References:
    """
    # TODO: Provide references in the doc above.


def theory_proves_proposition_external_algorithm(p: as1.Tupl | None = None, a: as1.Tupl | None = None):
    """An external algorithm for the t-proves-p (T ⊢ P) transformation.

    This algorithm is used to implement the syntactic-entailment inference-rule.

    Algorithm inputs:
     T: a theory
     P: a formula
    Algorithm:
     If T is a well-formed theory
     If P is a well-formed formula
     If P is a valid proposition in T
    Output:
     T ⊢ P
    Otherwise raise an error.

    :param p: Premises.
    :param a: Complementary arguments.
    :return:
    """
    p: as1.Tupl = as1.coerce_tuple(t=p)
    a: as1.Tupl = as1.coerce_tuple(t=a)
    if not a.arity == 2:
        raise u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
    t: as1.Theory = as1.coerce_theory(t=a[0], interpret_none_as_empty=False, canonical_conversion=False)
    p2: as1.Formula = as1.coerce_formula(phi=a[1])
    if as1.is_valid_proposition_in_theory_1(p=p2, t=t):
        phi: as1.Formula = t | as1.proves_connective | p2
        return phi
    else:
        raise u1.ApplicativeError(
            msg='Blablabla',
            code=None,
            p=p,
            a=a,
            t=t,
            p2=p2
        )


# INFERENCE-RULE: t-proves-p: T ⊢ P
with as1.let_x_be_a_variable(formula_ts='T') as t, as1.let_x_be_a_variable(formula_ts='P') as p:
    _t_proves_p: as1.TransformationByExternalAlgorithm = as1.let_x_be_a_transformation_by_external_algorithm(
        algo=theory_proves_proposition_external_algorithm,
        check=None,
        i=(
            as1.is_well_formed_theory_connective(t),),
        o=t | as1.proves_connective | p,
        v=(p, t,))
    t_proves_p: as1.InferenceRule = as1.InferenceRule(
        f=_t_proves_p,
        ref_ts=pl1.Monospace(text='T ⊢ P'))
    """The t-proves-p inference rule: T ⊢ P

    Abbreviation: T ⊢ P

    Premises:
     1. is-a-well-formed-theory(T)

    *. This premise is expressed in the object-theory T, and not in the current meta-theory.
       This means that we must be able to express premises in an object-theory.
       The data-model of premises must evolve to allow expressing T.P.
       TODO: One idea: 
    
    Conclusion: T ⊢ P

    References:
    """
    # TODO: Provide references in the doc above.
    pass

meta_theory_1 = as1.Axiomatization(d=(mt1, mt2, mt3, inconsistency_1, t_proves_p))
pass


def extend_theory_with_meta_theory_1(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with:
     - the meta-theory-1 axioms

    """
    global mt1, mt2, mt3, inconsistency_1
    t: as1.Theory = as1.coerce_theory(t=t)
    t, _ = as1.let_x_be_an_axiom(a=mt1, t=t)
    t, _ = as1.let_x_be_an_axiom(a=mt2, t=t)
    t, _ = as1.let_x_be_an_axiom(a=mt3, t=t)
    t, _ = as1.let_x_be_an_axiom(a=inconsistency_1, t=t)
    t, _ = as1.let_x_be_an_axiom(a=t_proves_p, t=t)
    # t.heuristics.add(p_is_a_proposition_heuristic)
    return t


pass
