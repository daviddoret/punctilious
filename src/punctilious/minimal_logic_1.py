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

# python native modules
import typing
# punctilious modules
import axiomatic_system_1 as as1
import inference_rules_1 as ir1


# Propositional logic vocabulary

class Connectives(typing.NamedTuple):
    implies: as1.BinaryConnective
    land: as1.BinaryConnective
    lnot: as1.UnaryConnective
    propositional_variable: as1.SimpleObject


connectives: Connectives = Connectives(
    implies=as1.connectives.implies,
    land=as1.connectives.land,
    lnot=as1.connectives.lnot,
    propositional_variable=as1.connectives.propositional_variable,
)

# retrieve vocabulary from axiomatic-system-1
is_a = as1.connectives.is_a
implies = as1.connectives.implies
land = as1.connectives.land
lnot = as1.connectives.lnot
propositional_variable = as1.connectives.propositional_variable
proposition = as1.connectives.proposition

with as1.let_x_be_a_variable(formula_typesetter='A') as a:
    pl01: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,),
            conclusion=a | implies | (a | land | a),
            variables=(a,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(formula_typesetter='b') as b:
    pl02: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition,),
            conclusion=(a | land | b) | implies | (b | land | a),
            variables=(a, b,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b, as1.let_x_be_a_variable(
    formula_typesetter='c') as c:
    pl03: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition,
             c | is_a | proposition),
            conclusion=(a | implies | b) | implies | ((a | land | c) | implies | (b | land | c)),
            variables=(a, b, c,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b, as1.let_x_be_a_variable(
    formula_typesetter='c') as c:
    pl04: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition,
             c | is_a | proposition),
            conclusion=((a | implies | b) | land | ((b | implies | c)) | implies | (a | implies | c)),
            variables=(a, b, c,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b:
    pl05: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=b | implies | (a | implies | b),
            variables=(a, b,)))
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

# - PL6. (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵
# - PL7. 𝐴 ⊃ (𝐴 ∨ 𝐵)
# - PL8. (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)
# - PL9. [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]
# - PL10. [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴

axiomatization = as1.Axiomatization(derivations=(pl01, pl02, pl03, pl04,))

extended_theory = as1.Theory(derivations=(*axiomatization,))

pass
