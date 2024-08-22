# import typing
import sys

import constants_1 as c1
import util_1 as u1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')


def is_well_formed_formula_algorithm(
        i: as1.WellFormedTupl | None = None,
        raise_error_if_false: bool = True) -> [bool, as1.WellFormedFormula | None]:
    """A python-function used as a formula external algorithm to verify is-well-formed-formula of a formula.

    :param i: A tuple of formulas, denoted as the input values.
    :param raise_error_if_false: If `True`, raises an error instead of returning `False, None`.
    :return: `True, o` where `o` is the algorithm output formula, or `False, None` if the transformation is not valid.
    """
    i: as1.WellFormedTupl = as1.coerce_tuple(s=i, interpret_none_as_empty=False, canonic_conversion=False)
    if not i.arity == 1:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_MT1_007,
                msg='is-well-formed-formula algorithm failure: '
                    'The number of input-values provided to the algorithm is not equal to 1.',
                i=i)
        else:
            return False, None
    phi: as1.WellFormedFormula = as1.coerce_formula(phi=i[0])
    if as1.is_well_formed_formula(phi=phi):
        phi: as1.WellFormedFormula = as1.connective_for_is_well_formed_formula(phi)
        return True, phi
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='is-well-formed-formula algorithm failure: '
                    'The argument `i[0]` is not a well-formed formula. '
                    'It follows that the statement :math:`\\text{is-well-formed-formula}(a_{0})` cannot be derived.',
                code=c1.ERROR_CODE_MT1_008,
                i0=i[0],
                phi=phi,
                i=i
            )
        else:
            return False, None


is_well_formed_formula_algorithm_connective: as1.ConnectiveLinkedWithAlgorithm = as1.ConnectiveLinkedWithAlgorithm(
    a=is_well_formed_formula_algorithm,
    formula_ts=pl1.Monospace(text='is-well-formed-formula-algorithm')
)


def is_well_formed_inference_rule_algorithm(
        i: as1.WellFormedTupl | None = None,
        raise_error_if_false: bool = True) -> [bool, as1.WellFormedFormula | None]:
    """A python-function used as a inference-rule external algorithm to verify is-well-formed-inference-rule of a formula.

    :param i: A tuple of formulas, denoted as the input values.
    :param raise_error_if_false: If `True`, raises an error instead of returning `False, None`.
    :return: `True, o` where `o` is the algorithm output formula, or `False, None` if the transformation is not valid.
    """
    i: as1.WellFormedTupl = as1.coerce_tuple(s=i, interpret_none_as_empty=False, canonic_conversion=False)
    if not i.arity == 1:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_MT1_005,
                msg='is-well-formed-inference-rule algorithm failure: '
                    'The number of input-values provided to the algorithm is not equal to 1.',
                i=i)
        else:
            return False, None
    ir: as1.WellFormedFormula = as1.coerce_formula(phi=i[0])
    if as1.is_well_formed_inference_rule(i=ir):
        ir: as1.WellFormedInferenceRule = as1.coerce_inference_rule(i=ir)
        phi: as1.WellFormedFormula = as1.connective_for_is_well_formed_inference_rule(ir)
        return True, phi
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='is-well-formed-inference-rule algorithm failure: '
                    'The argument `i[0]` is not a well-formed inference-rule. '
                    'It follows that the statement :math:`\\text{is-well-formed-inference-rule}(a_{0})` '
                    'cannot be derived.',
                code=c1.ERROR_CODE_MT1_006,
                i0=i[0],
                ir=ir,
                i=i
            )
        else:
            return False, None


is_well_formed_inference_rule_algorithm_connective: as1.ConnectiveLinkedWithAlgorithm = as1.ConnectiveLinkedWithAlgorithm(
    a=is_well_formed_inference_rule_algorithm,
    formula_ts=pl1.Monospace(text='is-well-formed-inference-rule-algorithm')
)


def is_well_formed_theory_algorithm(
        i: as1.WellFormedTupl | None = None,
        raise_error_if_false: bool = True) -> [bool, as1.WellFormedFormula | None]:
    """A python-function used as a theory external algorithm to verify is-well-formed-theory of a formula.

    :param i: A tuple of formulas, denoted as the input values.
    :param raise_error_if_false: If `True`, raises an error instead of returning `False, None`.
    :return: `True, o` where `o` is the algorithm output formula, or `False, None` if the transformation is not valid.
    """
    i: as1.WellFormedTupl = as1.coerce_tuple(s=i, interpret_none_as_empty=False, canonic_conversion=False)
    if not i.arity == 1:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_MT1_004,
                msg='is-well-formed-theory algorithm failure: '
                    'The number of input-values provided to the algorithm is not equal to 1.',
                i=i)
        else:
            return False, None
    t1: as1.WellFormedFormula = as1.coerce_formula(phi=i[0])
    if as1.is_well_formed_theory(t=t1):
        t1: as1.WellFormedTheory = as1.coerce_theory(t=t1, interpret_none_as_empty=False, canonical_conversion=False)
        phi: as1.WellFormedFormula = as1.connective_for_is_well_formed_theory(t1)
        return True, phi
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='is-well-formed-theory algorithm failure: '
                    'The argument `i[0]` is not a well-formed theory. '
                    'It follows that the statement :math:`\\text{is-well-formed-theory}(a_{0})` cannot be derived.',
                code=c1.ERROR_CODE_MT1_002,
                i0=i[0],
                t1=t1,
                i=i
            )
        else:
            return False, None


is_well_formed_theory_algorithm_connective: as1.ConnectiveLinkedWithAlgorithm = as1.ConnectiveLinkedWithAlgorithm(
    a=is_well_formed_theory_algorithm,
    formula_ts=pl1.Monospace(text='is-well-formed-theory-algorithm')
)

with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='phi')) as phi:
    algo: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=is_well_formed_formula_algorithm_connective,
        o=as1.connective_for_is_well_formed_formula(phi),
        v={phi, },
        i=(phi,),
        d=None)
    mt1: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=algo,
        ref_ts=pl1.Monospace(text='MT1'))
    """The is-well-formed-formula algorithmic inference-rule.

    Abbreviation: MT1

    Variables: {phi}

    Arguments: {phi}

    Premises:
    None

    Conclusion: 
     - is-well-formed-formula(phi)
    """

with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='i')) as i:
    algo: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=is_well_formed_inference_rule_algorithm_connective,
        o=as1.connective_for_is_well_formed_inference_rule(i),
        v={i, },
        i=(i,),
        d=None)
    mt2: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=algo,
        ref_ts=pl1.Monospace(text='MT2'))
    """The is-well-formed-inference-rule(i) inference rule.

    Abbreviation: MT2

    Variables: {i}

    Arguments: {i}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theory(i)
    """

# INFERENCE-RULE: MT3: is-well-formed-theory
with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as i:
    _mt3: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=is_well_formed_theory_algorithm_connective,
        # check=None,  # is_compatible_with_is_well_formed_theory
        o=as1.connective_for_is_well_formed_theory(i),
        i=(i,),
        v={i, },
        d=None)  # {t, })
    mt3: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
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
with as1.let_x_be_a_variable(formula_ts='T') as i, as1.let_x_be_a_variable(formula_ts='P') as p:
    inconsistency_1: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=as1.let_x_be_a_transformation_by_variable_substitution(
            i=(
                as1.connective_for_is_well_formed_theory(i),
                i | as1.connective_for_proves | p,
                i | as1.connective_for_proves | as1.connective_for_logical_negation(p)),
            o=as1.connective_for_is_inconsistent(i),
            v={p, i, }),
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


def theory_proves_proposition_algorithm(
        i: as1.WellFormedTupl | None = None,
        raise_error_if_false: bool = True) -> [bool, as1.WellFormedFormula | None]:
    """An external algorithm for the t-proves-p (T ⊢ P) transformation.

    This algorithm is used to implement the syntactic-entailment inference-rule.

    Algorithm inputs:
     q: is-well-formed-theory(T)
     P: a formula
    Algorithm:
     If T is a well-formed theory
     If P is a well-formed formula
     If P is a valid proposition in T
    Output:
     T ⊢ P
    Otherwise raise an error.

    :param i: A tuple of formulas, denoted as the input-values.
    :param raise_error_if_false:
    :return:
    """
    i: as1.WellFormedTupl = as1.coerce_tuple(s=i)
    if not i.arity == 2:
        if raise_error_if_false:
            raise u1.ApplicativeError(msg='wrong arguments', iv=i)
        else:
            return False, None
    p: as1.WellFormedFormula = as1.coerce_formula(phi=i[1])
    is_well_formed_theory_t: as1.WellFormedFormula = as1.coerce_formula(phi=i[0])
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        shape: as1.WellFormedFormula = as1.connective_for_is_well_formed_theory(x)
        ok, m = as1.is_formula_equivalent_with_variables_2(phi=is_well_formed_theory_t,
                                                           psi=shape,
                                                           variables={x, })
        if not ok:
            raise u1.ApplicativeError(msg='wrong input value i0', is_well_formed_theory_t=is_well_formed_theory_t,
                                      iv=i)
    t: as1.WellFormedFormula = is_well_formed_theory_t[0]
    t: as1.WellFormedTheory = as1.coerce_theory(t=t, interpret_none_as_empty=False, canonical_conversion=False)
    if as1.is_valid_proposition_so_far_1(p=p, t=t):
        # Proposition p is valid in the object-theory t.
        phi: as1.WellFormedFormula = t | as1.connective_for_proves | p
        return True, phi
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='Blablabla',
                code=None,
                iv=i,
                t=t,
                p2=p
            )
        else:
            return False, None


theory_proves_proposition_algorithm_connective: as1.ConnectiveLinkedWithAlgorithm = as1.ConnectiveLinkedWithAlgorithm(
    a=theory_proves_proposition_algorithm,
    formula_ts=pl1.Monospace(text='theory-proves-proposition-algorithm')
)

# INFERENCE-RULE: t-proves-p: T ⊢ P

with as1.let_x_be_a_variable(formula_ts='T') as i, as1.let_x_be_a_variable(formula_ts='P') as p:
    _t_proves_p: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=theory_proves_proposition_algorithm_connective,
        i=(
            as1.connective_for_is_well_formed_theory(i),
            p,),
        o=i | as1.connective_for_proves | p,
        v=(p, i,))
    t_proves_p: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
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

meta_theory_1 = as1.WellFormedAxiomatization(d=(mt1, mt2, mt3, t_proves_p, inconsistency_1,))
pass


def extend_theory_with_meta_theory_1(t: as1.FlexibleTheory) -> as1.WellFormedTheory:
    """Extends a theory with:
     - the meta-theory-1 axioms

    """
    global mt1, mt2, mt3, inconsistency_1
    t: as1.WellFormedTheory = as1.coerce_theory(t=t)
    t, _ = as1.let_x_be_an_axiom(a=mt1, t=t)
    t, _ = as1.let_x_be_an_axiom(a=mt2, t=t)
    t, _ = as1.let_x_be_an_axiom(a=mt3, t=t)
    t, _ = as1.let_x_be_an_axiom(a=t_proves_p, t=t)
    t, _ = as1.let_x_be_an_axiom(a=inconsistency_1, t=t)
    # t.heuristics.add(p_is_a_proposition_heuristic)
    return t


pass
