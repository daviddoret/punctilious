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


def is_well_formed_theoretical_context_algorithm(
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
                msg='is-well-formed-theoretical-context algorithm failure: '
                    'The number of input-values provided to the algorithm is not equal to 1.',
                i=i)
        else:
            return False, None
    t1: as1.WellFormedFormula = as1.coerce_formula(phi=i[0])
    if as1.is_well_formed_theoretical_context(t=t1):
        t1: as1.WellFormedTheoreticalContext = as1.coerce_theoretical_context(t=t1, interpret_none_as_empty=False,
                                                                              canonical_conversion=False)
        phi: as1.WellFormedFormula = as1.connective_for_is_well_formed_theoretical_context(t1)
        return True, phi
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='is-well-formed-theoretical-context algorithm failure: '
                    'The argument `i[0]` is not a well-formed theoretical-context. '
                    'It follows that the statement :math:`\\text{is-well-formed-theoretical-context}(a_{0})` '
                    'cannot be derived.',
                code=c1.ERROR_CODE_MT1_002,
                i0=i[0],
                t1=t1,
                i=i
            )
        else:
            return False, None


is_well_formed_theoretical_context_algorithm_connective: as1.ConnectiveLinkedWithAlgorithm = (
    as1.ConnectiveLinkedWithAlgorithm(
        a=is_well_formed_theoretical_context_algorithm,
        formula_ts=pl1.Monospace(text='is-well-formed-theoretical-context-algorithm')
    ))

with as1.let_x_be_a_variable(formula_ts=pl1.symbols.phi_lowercase_serif_bold) as phi:
    _mt1a: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=is_well_formed_formula_algorithm_connective,
        o=as1.connective_for_is_well_formed_formula(phi),
        v={phi, },
        i=(phi,),
        d=None)
    mt1a: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=_mt1a,
        ref_ts=pl1.Monospace(text='MT1a'))
    """The is-well-formed-formula inference-rule.

    Abbreviation: MT1a

    Variables: :math:`\\{𝞅\\}`

    Arguments: :math:`\\{𝞅\\}`

    Premises:
    None
    
    Algorithm:
    :func:`is_well_formed_formula_algorithm`

    Conclusion: 
    :math:`is-well-formed-formula(𝞅)`
    """

with as1.let_x_be_a_variable(formula_ts=pl1.symbols.phi_lowercase_serif_bold) as phi:
    mt1b: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=as1.WellFormedTransformationByVariableSubstitution(
            i=(as1.connective_for_is_well_formed_formula(phi),),
            o=as1.connective_for_is_well_formed_proposition(as1.connective_for_is_well_formed_formula(phi)),
            v=(phi,)),
        ref_ts=pl1.Monospace(text='MT1b'))
    """Axiom schema: 
        :math:`\\text{is-a-well-formed-formula}(𝞅) \\implies 
        \\text{is-a-well-formed-proposition}(\\text{is-a-well-formed-formula}(𝞅))`

    Premises:
     - :math:`\\text{is-a-well-formed-formula}(𝞅)`

    Variables:
    :math:`{ 𝞅 }`

    Conclusion: 
    :math:`\\text{is-a-well-formed-proposition}(\\text{is-a-well-formed-formula}(𝞅))` 

    Note 1:
    ⌜ :math:`\\text{is-a-well-formed-formula}` ⌝ is a predicate. It follows that 
    ⌜ :math:`\\text{is-a-well-formed-formula}(𝞅)` ⌝, where :math:`𝞅` is a variable, 
    is a well-formed proposition.
    
    Note 2:
    The Punctilious package only allows the manipulation of well-formed formulas,
    which leads to the situation that :math:`\\text{is-a-well-formed-formula}(𝞅)` is always valid.
    """
    pass

with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='i')) as i:
    _mt2a: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=is_well_formed_inference_rule_algorithm_connective,
        o=as1.connective_for_is_well_formed_inference_rule(i),
        v={i, },
        i=(i,),
        d=None)
    mt2a: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=_mt2a,
        ref_ts=pl1.Monospace(text='MT2'))
    """The is-well-formed-inference-rule(i) inference rule.

    Abbreviation: MT2

    Variables: {i}

    Arguments: {i}

    Premises:
    None

    Conclusion: 
     - is-well-formed-inference-rule(i)
    """

with as1.let_x_be_a_variable(formula_ts=pl1.symbols.phi_lowercase_serif_bold) as phi:
    mt2b: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=as1.WellFormedTransformationByVariableSubstitution(
            i=(as1.connective_for_is_well_formed_inference_rule(phi),),
            o=as1.connective_for_is_well_formed_proposition(as1.connective_for_is_well_formed_inference_rule(phi)),
            v=(phi,)),
        ref_ts=pl1.Monospace(text='MT2b'))
    """Axiom schema: 
        :math:`\\text{is-a-well-formed-inference-rule}(𝞅) \\implies 
        \\text{is-a-well-formed-proposition}(\\text{is-a-well-formed-inference-rule}(𝞅))`

    Premises:
     - :math:`\\text{is-a-well-formed-inference-rule}(𝞅)`

    Variables:
    :math:`{ 𝞅 }`

    Conclusion: 
    :math:`\\text{is-a-well-formed-proposition}(\\text{is-a-well-formed-inference-rule}(𝞅))` 

    Note 1:
    ⌜ :math:`\\text{is-a-well-formed-inference-rule}` ⌝ is a predicate. It follows that 
    ⌜ :math:`\\text{is-a-well-formed-inference-rule}(𝞅)` ⌝, where :math:`𝞅` is a variable, 
    is a well-formed proposition.
    """
    pass

# INFERENCE-RULE: MT3: is-well-formed-theory
with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='t')) as i:
    _mt3: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=is_well_formed_theoretical_context_algorithm_connective,
        o=as1.connective_for_is_well_formed_theoretical_context(i),
        i=(i,),
        v={i, },
        d=None)  # {t, })
    mt3a: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=_mt3,
        ref_ts=pl1.Monospace(text='MT3a'))
    """The is-well-formed-theoretical-context algorithmic inference-rule.

    Abbreviation: MT3a

    Variables: {t}

    Arguments: {t}

    Premises:
    None

    Conclusion: 
     - is-well-formed-theoretical-context(t)
    """

with as1.let_x_be_a_variable(formula_ts=pl1.symbols.phi_lowercase_serif_bold) as phi:
    mt3b: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=as1.WellFormedTransformationByVariableSubstitution(
            i=(as1.connective_for_is_well_formed_theoretical_context(phi)),
            o=as1.connective_for_is_well_formed_proposition(as1.connective_for_is_well_formed_theoretical_context(phi)),
            v=(phi,)),
        ref_ts=pl1.Monospace(text='MT3b'))
    """Axiom schema: 
        :math:`\\text{is-a-well-formed-theoretical-context}(𝞅) \\implies 
        \\text{is-a-well-formed-proposition}(\\text{is-a-well-formed-theoretical-context}(𝞅))`

    Premises:
    N/A

    Variables:
    :math:`{ 𝞅 }`

    Conclusion: 
    :math:`\\text{is-a-well-formed-proposition}(\\text{is-a-well-formed-theoretical-context}(𝞿))` 

    Note 1:
    ⌜ :math:`\\text{is-a-well-formed-theoretical-context}` ⌝ is a predicate. It follows that 
    ⌜ :math:`\\text{is-a-well-formed-theoretical-context}(𝞅)` ⌝, where :math:`𝞅` is a variable, 
    is a well-formed proposition.
    """
    pass

# INFERENCE-RULE: ⊥1: inconsistency-1: P and ¬P
with as1.let_x_be_a_variable(formula_ts='T') as i, as1.let_x_be_a_variable(formula_ts='P') as p:
    inconsistency_1: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=as1.let_x_be_a_transformation_by_variable_substitution(
            i=(
                as1.connective_for_is_well_formed_theoretical_context(i),
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


def theoretical_context_proves_proposition_algorithm(
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
            raise u1.ApplicativeError(
                msg='Wrong input-values. This algorithm expects a tuple of input-values `i` '
                    'of arity strictly equal to 2.',
                i_arity=i.arity,
                i=i)
        else:
            return False, None
    i0: as1.WellFormedFormula = as1.coerce_formula(phi=i[0])  # is-well-formed-theoretical-context(T)
    i1: as1.WellFormedFormula = as1.coerce_formula(phi=i[1])  # P
    with as1.let_x_be_a_variable(formula_ts='x') as x:
        v = {x, }
        s: as1.WellFormedFormula = as1.connective_for_is_well_formed_theoretical_context(x)
        ok, m = as1.is_formula_equivalent_with_variables_2(phi=i0,
                                                           psi=s,
                                                           variables=v)
        if not ok:
            raise u1.ApplicativeError(
                msg='The input-value `i0` with index 0 is wrong. Its expected shape is `s` with variables `v`. '
                    'It follows that `i0` should be formula-equivalent to `s` with variables `v` '
                    'but this is not the case.',
                i0=i0,
                s=s,
                v=v,
                i=i)
    t: as1.WellFormedFormula = i0[0]
    t: as1.WellFormedTheoreticalContext = as1.coerce_theoretical_context(t=t, interpret_none_as_empty=False,
                                                                         canonical_conversion=False)
    if as1.is_valid_proposition_so_far_1(p=i1, t=t):
        # Proposition p is valid in the object-theory t.
        phi: as1.WellFormedFormula = t | as1.connective_for_proves | i1
        return True, phi
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='`p` is not proven as a valid proposition in `t`.',
                p=i1,
                iv=i,
                t=t
            )
        else:
            return False, None


theoretical_context_proves_proposition_algorithm_connective: as1.ConnectiveLinkedWithAlgorithm = as1.ConnectiveLinkedWithAlgorithm(
    a=theoretical_context_proves_proposition_algorithm,
    formula_ts=pl1.Monospace(text='theoretical-context-proves-proposition-algorithm')
)

# INFERENCE-RULE: t-proves-p: T ⊢ P

with (as1.let_x_be_a_variable(formula_ts='T') as i, as1.let_x_be_a_variable(formula_ts='P') as p):
    _t_proves_p: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        a=theoretical_context_proves_proposition_algorithm_connective,
        i=(
            as1.connective_for_is_well_formed_theoretical_context(i),
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

meta_theory_1 = as1.let_x_be_an_axiomatization(d=(mt1a, mt1b, mt2a, mt2b, mt3a, mt3b, t_proves_p, inconsistency_1,),
                                               ref_ts=pl1.Script(text='MT1'))
pass


def extend_theory_with_meta_theory_1(t: as1.FlexibleTheoreticalContext) -> as1.WellFormedTheoreticalContext:
    """Extends a theory with:
     - the meta-theory-1 axioms

    """
    global meta_theory_1
    t: as1.WellFormedTheoreticalContext = as1.coerce_theoretical_context(t=t)
    x: as1.WellFormedExtension = as1.WellFormedExtension(t=meta_theory_1)
    t = as1.extend_with_component(t=t, c=x)
    return t


pass
