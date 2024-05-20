"""This module elaborates an axiomatization of minimal-logic.

Original definition:
"Definition 2.2. The formulas are defined as follows:
1. Basis clause: Each propositional variable is a formula (called an atomic formula).
2. Inductive clause: If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵).
3. Extremal clause: Nothing else is a formula." (Mancosu et al., 2021, p. 14.)

Bibliography:
 - Mancosu et al., 2021
"""

# python native modules
import typing
# punctilious modules
import axiomatic_system_1 as as1
import inference_rules_1 as ir1

# Propositional logic vocabulary


# retrieve vocabulary from axiomatic-system-1
is_a = as1.connectives.is_a
implies = as1.connectives.implies
land = as1.connectives.land
lnot = as1.connectives.lnot
lor = as1.connectives.lor
proposition = as1.connectives.proposition  # synonym: propositional-formulas
propositional_variable = as1.connectives.propositional_variable

with as1.let_x_be_a_variable(rep='A') as a:
    i1: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | propositional_variable,),
            conclusion=a | is_a | proposition,
            variables=(a,)))
    """A is-a propositional-variable ⊃ A is a proposition
    
    Original definition: 
    "Each propositional variable is a formula" (Mancosu et al., 2021)
    """
    pass

with as1.let_x_be_a_variable(rep='A') as a:
    i2: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,),
            conclusion=lnot(a) | is_a | proposition,
            variables=(a,)))
    """A is-a proposition ⊃ ¬A is a proposition
    
    Original definition: 
    "If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵)" (Mancosu et al., 2021)
    """
    pass

with as1.let_x_be_a_variable(rep='A') as a, as1.let_x_be_a_variable(rep='B') as b:
    i3: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | land | b) | is_a | proposition,
            variables=(a, b,)))
    """(A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition)

    Original definition: 
    "If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵)" (Mancosu et al., 2021)
    """
    pass

with as1.let_x_be_a_variable(rep='A') as a, as1.let_x_be_a_variable(rep='B') as b:
    i4: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | implies | b) | is_a | proposition,
            variables=(a,)))
    pass

with as1.let_x_be_a_variable(rep='A') as a, as1.let_x_be_a_variable(rep='B') as b:
    i5: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | lor | b) | is_a | proposition,
            variables=(a,)))
    pass

axioms = as1.Axiomatization(axioms=(i1, i2, i3, i4, i5,))

extended_theory = as1.Demonstration(theorems=(*axioms,))

pass
