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

import typing
import axiomatic_system_1 as as1
import propositional_logic_syntax_1 as pls1

# Propositional logic vocabulary


# retrieve vocabulary from axiomatic-system-1
is_a = as1.connectives.is_a
implies = as1.connectives.implies
land = as1.connectives.land
lor = as1.connectives.lor
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

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(formula_typesetter='B') as b:
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

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(
        formula_typesetter='B') as b, as1.let_x_be_a_variable(
    formula_typesetter='C') as c:
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

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(
        formula_typesetter='B') as b, as1.let_x_be_a_variable(
    formula_typesetter='C') as c:
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b:
    pl06: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(b | land | (a | implies | b)) | implies | b,
            variables=(a, b,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b:
    pl07: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=a | implies | (a | lor | b),
            variables=(a, b,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b:
    pl08: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | lor | b) | implies | (b | lor | a),
            variables=(a, b,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b:
    pl09: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition,
             c | is_a | proposition),
            conclusion=((a | implies | c) | land | (b | implies | c)) | implies | ((a | lor | b) | implies | c),
            variables=(a, b,)))
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

with as1.let_x_be_a_variable(formula_typesetter='a') as a, as1.let_x_be_a_variable(
        formula_typesetter='b') as b:
    pl10: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=((a | implies | b) | land | (a | implies | lnot(b))) | implies | lnot(a),
            variables=(a, b,)))
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

axiomatization = as1.Axiomatization(derivations=(pl01, pl02, pl03, pl04, pl05, pl06, pl07, pl08, pl09, pl10))

extended_theory = as1.Theory(derivations=(*axiomatization,))


def extend_theory_with_minimal_logic_1(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with:
     - the propositional-logic-syntax-1 axioms,
     - the minimal-logic-1 axioms,
     - TODO: add some theory-specific heuristics?

    """
    global pl01, pl02, pl03, pl04, pl05, pl06, pl07, pl08, pl09, pl10
    t: as1.Theory = as1.coerce_theory(phi=t)
    t: as1.Theory = pls1.extend_theory_with_propositional_logic_syntax_1(t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl01, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl02, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl03, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl04, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl05, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl06, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl07, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl08, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl09, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=pl10, t=t)
    return t


def let_x_be_a_minimal_logic_1_theory() -> as1.Theory:
    """Return a new theory with:
     - the propositional-logic-syntax-1 axioms,
     - the minimal-logic-1 axioms,
     - TODO: add some theory-specific heuristics?
     """
    t: as1.Theory = as1.Theory()
    t = extend_theory_with_minimal_logic_1(t=t)
    return t
