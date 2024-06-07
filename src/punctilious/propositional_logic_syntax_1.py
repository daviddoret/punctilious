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

with as1.let_x_be_a_variable(formula_typesetter='A') as a:
    i1: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | propositional_variable,),
            conclusion=a | is_a | proposition,
            variables=(a,)))
    """Axiom schema: A is-a propositional-variable ⊃ A is-a proposition.
    
    Premises:
     - A is-a propositional-variable

    Conclusion: 
    A is-a proposition

    Variables:
    {A}

    Original axiom: 
    "Each propositional variable is a formula" (Mancosu et al., 2021).
    """
    pass

with as1.let_x_be_a_variable(formula_typesetter='A') as a:
    i2: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,),
            conclusion=lnot(a) | is_a | proposition,
            variables=(a,)))
    """Axiom schema: A is-a proposition ⊃ ¬A is a proposition.

    Premises:
     - A is-a proposition

    Conclusion: 
    ¬A is a proposition

    Variables:
    {A}

    Original axiom: 
    "If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵)" (Mancosu et al., 2021).
    """
    pass

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(formula_typesetter='B') as b:
    i3: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | land | b) | is_a | proposition,
            variables=(a, b,)))
    """Axiom schema: (A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition).

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    (A ∧ B) is a proposition

    Variables:
    {A, B}

    Original axiom: 
    "If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵)" (Mancosu et al., 2021).
    """
    pass

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(formula_typesetter='B') as b:
    i4: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | implies | b) | is_a | proposition,
            variables=(a, b,)))
    """Axiom schema: (A is-a proposition, B is-a proposition) ⊃ ((A ⊃ B) is a proposition).

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    (A ⊃ B) is a proposition

    Variables:
    {A, B}

    Original axiom: 
    "If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵)" (Mancosu et al., 2021).
    """
    pass

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(formula_typesetter='B') as b:
    i5: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=
            (a | is_a | proposition,
             b | is_a | proposition),
            conclusion=(a | lor | b) | is_a | proposition,
            variables=(a, b,)))
    """Axiom schema: (A is-a proposition, B is-a proposition) ⊃ ((A ∨ B) is a proposition).

    Premises:
     - A is-a proposition
     - B is-a proposition

    Conclusion: 
    (A ∨ B) is a proposition

    Variables:
    {A, B}

    Original axiom: 
    "If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵)" (Mancosu et al., 2021).
    """
    pass

axioms = as1.Axiomatization(axioms=(i1, i2, i3, i4, i5,))

extended_theory = as1.Theory(derivations=(*axioms,))


def let_x_be_a_propositional_variable(
        theory: as1.FlexibleTheory,
        rep: as1.FlexibleRepresentation) -> \
        typing.Tuple[as1.Theory, as1.Variable | typing.Tuple[as1.Variable, ...]]:
    """Declare one or multiple propositional-variables in the input theory.

    If they are not already present, all axioms of propositional-logic-syntax-1 are appended to
    the theory.

    For every propositional-variable, the following axiom is automatically postulated in the theory:
     - x is-a propositional-variable
    ...and the following theorem is derived:
     - x is-a propositional

    The following

    :param theory:
    :param rep:
    :return:
    """
    global axioms
    global i1
    theory: as1.FlexibleTheory = as1.coerce_theory(phi=theory)

    # Include all propositional-logic-syntax-1 axioms if they are not already present
    # in the theory.
    for inference_rule in axioms:
        if not theory.has_element(inference_rule):
            theory, _ = as1.let_x_be_an_inference_rule(theory=theory, inference_rule=inference_rule)

    if isinstance(rep, str):
        # declare a single propositional variable
        x = as1.Variable(connective=as1.NullaryConnective(formula_typesetter=rep))
        theory, _ = as1.let_x_be_an_axiom(theory=theory,
                                          valid_statement=x | as1.connectives.is_a | as1.connectives.propositional_variable)
 
        return theory, x
    elif isinstance(rep, typing.Iterable):
        # declare multiple propositional variables
        propositional_variables = tuple()
        for r in rep:
            x = as1.Variable(connective=as1.NullaryConnective(formula_typesetter=r))
            propositional_variables = propositional_variables + (x,)
            theory, _ = as1.let_x_be_an_axiom(theory=theory,
                                              valid_statement=x | as1.connectives.is_a | as1.connectives.propositional_variable)
            theory, _ = as1.derive(theory=theory,
                                   valid_statement=x | is_a | proposition,
                                   premises=(x | as1.connectives.is_a | as1.connectives.propositional_variable,),
                                   inference_rule=i1)
        return theory, *propositional_variables
    else:
        raise TypeError  # TODO: Implement event code.


pass
