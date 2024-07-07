"""This module elaborates an axiomatization of minimal-logic.

Original axioms:
The following are the original axioms from Mancosu et al., 2021, p. 19:
 - PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)
 - PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)
 - PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]
 - PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)
 - PL5. 𝐵 ⊃ (𝐴 ⊃ 𝐵)
 - PL6. (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵
 - PL7. 𝐴 ⊃ (𝐴 ∨ 𝐵)
 - PL8. (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)
 - PL9. [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]
 - PL10. [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴

Implementation in axiomatic-system-1:
The axioms above are more specifically axiom-schemas rather than axioms. In axiomatic-system-1, axiom-schemas are
expressed as inference-rules. The axioms above are thus translated to equivalent axiomatic-system-1 transformations,
which are then included in inference-rules.

This translation is performed as follows:
 - for all propositional variable X in the original axiom, a premise X is-a propositional-variable is elaborated,
   this prevents the usage of the transformation with inadequate variables (e.g.: natural numbers instead of
   propositional-variables),
 - the antecedent of the original axiom implication is appended as a premise of the transformation,
 - for all propositional variable X in the original axiom, a variable is appended in the transformation variables
   enumeration.

The above has been implemented as an algorithm: the function translate_implication_to_axiom().

It would be technically possible to implement that as a native transformation, allowing to infer
the inference-rules from the original axioms. This is left as an exercise for later.

Bibliography:
 - Mancosu et al., 2021, p. 19.
"""

# import typing
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
from connectives_standard_library_1 import *
import inference_rules_1 as ir1
import propositional_logic_syntax_1 as pls1

# Propositional logic vocabulary


with as1.let_x_be_a_variable(formula_ts='A') as a:
    pl01: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,),
            conclusion=a | implies | (a | land | a),
            variables=(a,)),
        ref_ts=pl1.Monospace(text='PL1'))
    """The PL01 axiom schema: A ⊃ (A ∧ A).
    
    Premises:
     - A is-a proposition
    
    Conclusion: 
    A implies (A ∧ A)
    
    Variables:
    {A}
    
    Original axiom: 
    PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴). (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(formula_ts='B') as b:
    pl02: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition,),
            conclusion=(a | land | b) | implies | (b | land | a),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL2'))
    """The PL02 axiom schema: (A ∧ B) ⊃ (B ∧ A).

        Premises:
         - A is-a proposition
         - B is-a proposition

        Conclusion: 
        (A ∧ B) ⊃ (B ∧ A)

        Variables:
        {A, B}

        Original axiom: 
        PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴). (Mancosu et al., p. 19).
        """
    pass

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(
        formula_ts='B') as b, as1.let_x_be_a_variable(formula_ts='C') as c:
    pl03: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition,
                      c | is_a | proposition),
            conclusion=(a | implies | b) | implies | ((a | land | c) | implies | (b | land | c)),
            variables=(a, b, c,)),
        ref_ts=pl1.Monospace(text='PL3'))
    """The PL03 axiom schema: (A ⊃ B) ⊃ [(A ∧ C) ⊃ (B ∧ C)].
    
    Premises:
     - A is-a proposition
     - B is-a proposition
     - C is-a proposition
    
    Conclusion: 
    (A ⊃ B) ⊃ [(A ∧ C) ⊃ (B ∧ C)]
    
    Variables:
    {A, B, C}
    
    Original axiom: 
    PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]. (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(
        formula_ts='B') as b, as1.let_x_be_a_variable(formula_ts='C') as c:
    pl04: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition,
                      c | is_a | proposition),
            conclusion=((a | implies | b) | land | (b | implies | c) | implies | (a | implies | c)),
            variables=(a, b, c,)),
        ref_ts=pl1.Monospace(text='PL4'))
    """The PL04 axiom schema: [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶).

    Premises:
     - A is-a proposition
     - B is-a proposition
     - C is-a proposition

    Conclusion: 
    [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)

    Variables:
    {A, B, C}

    Original axiom: 
    PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶). (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='a') as a, as1.let_x_be_a_variable(
        formula_ts='b') as b:
    pl05: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=b | implies | (a | implies | b),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL5'))
    """The PL05 axiom schema: 𝐵 ⊃ (𝐴 ⊃ 𝐵).

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    𝐵 ⊃ (𝐴 ⊃ 𝐵)

    Variables:
    {A, B}

    Original axiom: 
    PL5. 𝐵 ⊃ (𝐴 ⊃ 𝐵). (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='a') as a, as1.let_x_be_a_variable(
        formula_ts='b') as b:
    pl06: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=(b | land | (a | implies | b)) | implies | b,
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL6'))
    """The PL06 axiom schema: (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵.

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵

    Variables:
    {A, B}

    Original axiom: 
    PL6. (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵. (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='a') as a, as1.let_x_be_a_variable(
        formula_ts='b') as b:
    pl07: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=a | implies | (a | lor | b),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL7'))
    """The PL07 axiom schema: 𝐴 ⊃ (𝐴 ∨ 𝐵).

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    𝐴 ⊃ (𝐴 ∨ 𝐵)

    Variables:
    {A, B}

    Original axiom: 
    PL7. 𝐴 ⊃ (𝐴 ∨ 𝐵). (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='a') as a, as1.let_x_be_a_variable(
        formula_ts='b') as b:
    pl08: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=(a | lor | b) | implies | (b | lor | a),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL8'))
    """The PL08 axiom schema: (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴).

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)

    Variables:
    {A, B}

    Original axiom: 
    PL8. (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴). (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='a') as a, as1.let_x_be_a_variable(
        formula_ts='b') as b:
    pl09: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition,
                      c | is_a | proposition),
            conclusion=((a | implies | c) | land | (b | implies | c)) | implies | ((a | lor | b) | implies | c),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL9'))
    """The PL09 axiom schema: [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶].

    Premises:
     - A is-a proposition
     - B is-a proposition
     - C is-a proposition

    Conclusion: 
    [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]

    Variables:
    {A, B, C}

    Original axiom: 
    PL9. [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]. (Mancosu et al., p. 19).
    """
    pass

with as1.let_x_be_a_variable(formula_ts='a') as a, as1.let_x_be_a_variable(
        formula_ts='b') as b:
    pl10: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=((a | implies | b) | land | (a | implies | lnot(b))) | implies | lnot(a),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PL10'))
    """The PL10 axiom schema:  [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴.

    Premises:
     - A is-a proposition
     - B is-a proposition
     - C is-a proposition

    Conclusion: 
    [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴

    Variables:
    {A, B, C}

    Original axiom: 
    PL10. [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴. (Mancosu et al., p. 19).
    """
    pass

axiomatization = as1.Axiomatization(d=(pl01, pl02, pl03, pl04, pl05, pl06, pl07, pl08, pl09, pl10))

extended_theory = as1.Theory(d=(*axiomatization,))


def extend_theory_with_minimal_logic_1(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with:
     - the propositional-logic-syntax-1 axioms,
     - the minimal-logic-1 axioms,
     - TODO: add some theory-specific heuristics?

    """
    global pl01, pl02, pl03, pl04, pl05, pl06, pl07, pl08, pl09, pl10
    t: as1.Theory = as1.coerce_theory(t=t)
    t: as1.Theory = pls1.extend_theory_with_propositional_logic_syntax_1(t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl01, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl02, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl03, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl04, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl05, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl06, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl07, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl08, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl09, t=t)
    t, _ = as1.let_x_be_an_axiom(a=pl10, t=t)
    return t


def extend_theory_with_mancosu_2021_page_20(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with Mancosu et al., page 20:
    1. ⊢ 𝑝1 ⊃ (𝑝1 ∨ 𝑝2) (axiom PL7)
    2. ⊢ [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] (axiom PL5)
    3. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) (mp 1, 2)
    4. ⊢ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] ⊃[{((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃
        {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))}] (axiom PL3)
    5. ⊢ {((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃ {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} (mp 3, 4)
    6. ⊢ [(𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] (axiom PL1)
    7. ⊢ (𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1) (axiom PL8)
    8. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) (mp 6, 7)
    9. ⊢ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) (mp 5, 8)
    10. ⊢ [((𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] ⊃ (𝑝1 ⊃ (𝑝2 ∨ 𝑝1)) (axiom PL4)
    11. ⊢ 𝑝1 ⊃ (𝑝2 ∨ 𝑝1) (mp 9, 10)

    :param t:
    :return:
    """
    global pl01, pl02, pl03, pl04, pl05, pl06, pl07, pl08, pl09, pl10
    t = extend_theory_with_minimal_logic_1(t=t)
    t, c, = pls1.let_x_be_a_propositional_variable(t=t, formula_ts='C')
    t, d, = pls1.let_x_be_a_propositional_variable(t=t, formula_ts='D')
    # TODO: Implement this as a proper hypothesis
    # TODO: Implement short reference names
    # 1. ⊢ 𝑝1 ⊃ (𝑝1 ∨ 𝑝2) (axiom PL7)
    # 2. ⊢ [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] (axiom PL5)
    # 3. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) (mp 1, 2)
    # 4. ⊢ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] ⊃[{((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃
    #     {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))}] (axiom PL3)
    # 5. ⊢ {((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃ {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} (mp 3, 4)
    # 6. ⊢ [(𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] (axiom PL1)
    # 7. ⊢ (𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1) (axiom PL8)
    # 8. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) (mp 6, 7)
    # 9. ⊢ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) (mp 5, 8)
    # 10. ⊢ [((𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] ⊃ (𝑝1 ⊃ (𝑝2 ∨ 𝑝1)) (axiom PL4)
    # 11. ⊢ 𝑝1 ⊃ (𝑝2 ∨ 𝑝1) (mp 9, 10)

    return t


def extend_theory_with_mancosu_2021_page_21(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with Mancosu et al., page 22:
        1. ⊢ 𝐶 (hypothesis)
        2. ⊢ 𝐶 ⊃ (𝐷 ⊃ 𝐶) (axiom PL5)
        3. ⊢ 𝐷 ⊃ 𝐶 (mp 1, 2)
        4. ⊢ (𝐷 ⊃ 𝐶) ⊃ [(𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)] (axiom PL3)
        5. ⊢ (𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷) (mp 3, 4)
        6. ⊢ 𝐷 ⊃ (𝐷 ∧ 𝐷) (axiom PL1)
        7. ⊢ 𝐷 (hypothesis)
        8. ⊢ 𝐷 ∧ 𝐷 (mp 6, 7)
        9. ⊢ 𝐶 ∧ 𝐷 (mp 5, 8)

    :param t:
    :return:
    """
    global pl01, pl02, pl03, pl04, pl05, pl06, pl07, pl08, pl09, pl10
    t = extend_theory_with_minimal_logic_1(t=t)
    t, c = pls1.let_x_be_a_propositional_variable(t=t, formula_ts='C')
    t, d = pls1.let_x_be_a_propositional_variable(t=t, formula_ts='D')
    t, success, _ = as1.derive_2(c=c | is_a | proposition,
                                 i=pls1.i1, t=t)
    t, success, _ = as1.derive_2(c=d | is_a | proposition,
                                 i=pls1.i1, t=t)
    t, success, _ = as1.derive_2(c=(c | implies | d) | is_a | proposition,
                                 i=pls1.i4, t=t)
    t, success, _ = as1.derive_2(c=(d | implies | c) | is_a | proposition,
                                 i=pls1.i4, t=t)
    t, success, _ = as1.derive_2(c=(d | land | d) | is_a | proposition,
                                 i=pls1.i3, t=t)
    t, success, _ = as1.derive_2(c=(c | land | d) | is_a | proposition,
                                 i=pls1.i3, t=t)
    t, success, _ = as1.derive_2(c=((d | land | d) | implies | (c | land | d)) | is_a | proposition,
                                 i=pls1.i4, t=t)
    # 1. ⊢ 𝐶(hypothesis)
    # TODO: Implement this as a proper hypothesis
    t, hypothesis = as1.let_x_be_an_axiom(t=t, s=c)
    # 2. ⊢ 𝐶 ⊃ (𝐷 ⊃ 𝐶)(axiom PL5)
    t, success, _, = as1.derive_2(c=c | implies | (d | implies | c),
                                  i=pl05, t=t)
    # 3. ⊢ 𝐷 ⊃ 𝐶 (mp 1, 2)
    t, success, _, = as1.derive_2(c=d | implies | c,
                                  i=ir1.modus_ponens, t=t)
    # 4. ⊢ (𝐷 ⊃ 𝐶) ⊃ [(𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)] (axiom PL3)
    t, success, _, = as1.derive_2(
        c=(d | implies | c) | implies | ((d | land | d) | implies | (c | land | d)),
        i=pl03, t=t)
    # 5. ⊢ (𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)(mp 3, 4)
    t, success, _, = as1.derive_2(
        c=(d | land | d) | implies | (c | land | d),
        i=ir1.modus_ponens, t=t)
    # 6. ⊢ 𝐷 ⊃ (𝐷 ∧ 𝐷)(axiom PL1)
    t, success, _, = as1.derive_2(
        c=d | implies | (d | land | d),
        i=pl01, t=t)
    # 7. ⊢ 𝐷(hypothesis)
    t, _, = as1.let_x_be_an_axiom(t=t, s=d)
    # 8. ⊢ 𝐷 ∧ 𝐷(mp 6, 7)
    t, success, _, = as1.derive_2(
        c=d | land | d,
        i=ir1.modus_ponens, t=t)
    # 9. ⊢ 𝐶 ∧ 𝐷(mp 5, 8)
    t, success, _, = as1.derive_2(
        c=c | land | d,
        i=ir1.modus_ponens, t=t, debug=False)

    return t


def let_x_be_a_minimal_logic_1_theory(**kwargs) -> as1.Theory:
    """Return a new theory with:
     - the propositional-logic-syntax-1 axioms,
     - the minimal-logic-1 axioms,
     - TODO: add some theory-specific heuristics?
     """
    # if 'formula_name_ts' not in kwargs:
    #    kwargs['formula_name_ts'] = pl1.IndexedSymbolTypesetter(body_ts=pl1.Script(text='M'), index=0)
    t: as1.Theory = as1.Theory(**kwargs)
    t = extend_theory_with_minimal_logic_1(t=t)
    return t
