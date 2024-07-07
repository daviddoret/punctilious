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
import util_1 as u1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
from connectives_standard_library_1 import *

# import inference_rules_1 as ir1

ERROR_CODE_PLS1_001 = 'E-PLS1-001'
ERROR_CODE_PLS1_002 = 'E-PLS1-002'
ERROR_CODE_PLS1_003 = 'E-PLS1-003'
ERROR_CODE_PLS1_004 = 'E-PLS1-004'
ERROR_CODE_PLS1_005 = 'E-PLS1-005'
ERROR_CODE_PLS1_006 = 'E-PLS1-006'
ERROR_CODE_PLS1_007 = 'E-PLS1-007'
ERROR_CODE_PLS1_008 = 'E-PLS1-008'
ERROR_CODE_PLS1_009 = 'E-PLS1-009'
ERROR_CODE_PLS1_010 = 'E-PLS1-010'

# Propositional logic vocabulary


with as1.let_x_be_a_variable(formula_ts='A') as a:
    i0: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            conclusion=a | is_a | propositional_variable,
            variables=None,
            declarations=(a,),
            premises=None
        ),
        ref_ts=pl1.Monospace(text='PLS1'))
    """Axiom schema: A is-a propositional-variable.

    Premises:
     - None
     
    Declarations of new objects:
     - A

    Conclusion: 
    A is-a proposition

    Variables:
     - None

    """
    pass

with as1.let_x_be_a_variable(formula_ts='A') as a:
    i1: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            premises=(a | is_a | propositional_variable,),
            conclusion=a | is_a | proposition,
            variables=(a,)),
        ref_ts=pl1.Monospace(text='PLS1'))
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

with as1.let_x_be_a_variable(formula_ts='A') as a:
    i2: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            premises=(a | is_a | proposition,),
            conclusion=lnot(a) | is_a | proposition,
            variables=(a,)),
        ref_ts=pl1.Monospace(text='PLS2'))
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

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(formula_ts='B') as b:
    i3: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=(a | land | b) | is_a | proposition,
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PLS3'))
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

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(formula_ts='B') as b:
    i4: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=(a | implies | b) | is_a | proposition,
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PLS4'))
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

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(formula_ts='B') as b:
    i5: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            premises=(a | is_a | proposition,
                      b | is_a | proposition),
            conclusion=(a | lor | b) | is_a | proposition,
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PLS5'))
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

with as1.let_x_be_a_variable(formula_ts='A') as a, as1.let_x_be_a_variable(formula_ts='B') as b:
    i6: as1.InferenceRule = as1.InferenceRule(
        t=as1.NaturalTransformation(
            premises=None,
            conclusion=lnot(a | is_a | proposition),
            variables=(a, b,)),
        ref_ts=pl1.Monospace(text='PLS6'))
    """Axiom schema: ?????.
    
    TODO: How could we implement the extreme case????????

    Premises:
    ?????

    Conclusion: 
    not (A is a proposition)

    Variables:
    {A}

    Original axiom: 
    "Extremal clause: Nothing else is a formula." (Mancosu et al., 2021).
    """
    pass

axiomatization = as1.Axiomatization(d=(i0, i1, i2, i3, i4, i5,))

extended_theory = as1.Theory(d=(*axiomatization,))


def let_x_be_a_propositional_variable(
        t: as1.FlexibleTheory, formula_ts: as1.FlexibleRepresentation) -> typing.Tuple[as1.Theory, as1.Variable]:
    """Declare a propositional-variable in theory t.

    If they are not already present, all axioms of propositional-logic-syntax-1 are appended to theory t.

    The following axiom is automatically postulated in theory t:
        (x is-a propositional-variable)

    :param t:
    :param formula_ts:
    :return:
    """
    global axiomatization
    global i0
    t: as1.FlexibleTheory = as1.coerce_theory(t=t)

    # Include all propositional-logic-syntax-1 axioms if they are not already present
    # in the theory.
    t = as1.append_to_theory(axiomatization, t=t)

    x = as1.Variable(c=as1.NullaryConnective(formula_ts=formula_ts))
    # t, _ = as1.let_x_be_an_axiom(t=t, s=x | as1._connectives.is_a | as1._connectives.propositional_variable)
    t, _ = as1.derive_1(t=t, c=x | as1._connectives.is_a | as1._connectives.propositional_variable,
                        p=None, i=i0)

    return t, x


def let_x_be_some_propositional_variables(
        t: as1.FlexibleTheory,
        ts: typing.Iterable[as1.FlexibleRepresentation]) -> typing.Tuple[as1.Theory, as1.Variable, ...]:
    """"""
    propositional_variables: tuple[as1.Variable, ...] = tuple()
    for ts in ts:
        t, x = let_x_be_a_propositional_variable(t=t, formula_ts=ts)
        propositional_variables = propositional_variables + (x,)
    return t, *propositional_variables


def translate_implication_to_axiom(t: as1.FlexibleTheory,
                                   phi: as1.FlexibleFormula) -> as1.InferenceRule:
    """Given a propositional formula phi that is an implication,
    translates phi to an equivalent axiomatic-system-1 inference-rule.

    Note: the initial need was to translate the original axioms of minimal-logic-1.

    :param t:
    :param phi:
    :return:
    """
    phi = as1.coerce_formula(phi=phi)
    if phi.connective is not as1._connectives.implies:
        raise u1.ApplicativeError(code=ERROR_CODE_PLS1_001, msg='this is not an implication')
    # TODO: translate_implication_to_axiom: check that all sub-formulas in phi are either:
    # - valid propositional formulas (negation, conjunction, etc.)
    # - atomic elements that can be mapped to propositional variables

    # Now we have the assurance that phi is a well-formed propositional formula.
    # Retrieve the list of propositional-variables in phi:
    propositional_variables: as1.Enumeration = as1.get_leaf_formulas(phi=phi)
    premises: as1.Enumeration = as1.Enumeration(elements=None)
    variables_map: as1.Map = as1.Map(domain=None, codomain=None)
    for x in propositional_variables:
        rep: str = x.typeset_as_string() + '\''
        # automatically append the axiom: x is-a propositional-variable
        with let_x_be_a_propositional_variable(t=t, formula_ts=rep) as x2:
            premises: as1.Enumeration = as1.append_element_to_enumeration(
                e=premises, x=x2 | as1._connectives.is_a | as1._connectives.propositional_variable)
            variables_map: as1.Map = as1.append_pair_to_map(m=variables_map, preimage=x, image=x2)
    variables: as1.Enumeration = as1.Enumeration(elements=variables_map.codomain)

    # elaborate a new formula psi where all variables have been replaced with the new variables
    psi = as1.replace_formulas(phi=phi, m=variables_map)

    # translate the antecedent of the implication to the main premises
    # note: we could further split conjunctions into multiple premises
    antecedent: as1.Formula = psi.term_0
    premises: as1.Enumeration = as1.append_element_to_enumeration(
        e=premises, x=antecedent)

    # retrieve the conclusion
    conclusion: as1.Formula = psi.term_1

    # build the rule
    rule: as1.NaturalTransformation = as1.NaturalTransformation(premises=premises, conclusion=conclusion,
                                                                variables=variables)

    # build the inference-rule
    inference_rule: as1.InferenceRule = as1.InferenceRule(t=rule)

    return inference_rule


class PIsAProposition(as1.Heuristic):

    def process_conjecture(self, conjecture: as1.FlexibleFormula, t: as1.FlexibleTheory) -> tuple[as1.Theory, bool,]:
        conjecture: as1.Formula = as1.coerce_formula(phi=conjecture)
        t: as1.Theory = as1.coerce_theory(t=t)

        t, success, _ = as1.derive_0(c=conjecture, t=t)
        if success:
            # The conjecture is already proven in the theory.
            return t, True

        with as1.let_x_be_a_meta_variable(formula_ts='P') as p:
            success, m = as1.is_formula_equivalent_with_variables_2(
                phi=conjecture, psi=p | is_a | proposition, variables=(p,))

            if success:
                # The conjecture is of the form (P is-a proposition).
                # Make an attempt to automatically derive the conjecture.

                # retrieve P's value
                p_value: as1.Formula = as1.get_image_from_map(m=m, preimage=p)

                if as1.is_valid_statement_in_theory(phi=p_value | is_a | propositional_variable, t=t):
                    # If P is a propositional-variable:
                    # We can safely derive p | is_a | proposition
                    t, _ = as1.derive_1(
                        c=p_value | is_a | proposition,
                        p=(
                            p_value | is_a | propositional_variable,),
                        i=i1, t=t)

                    return t, True

                with as1.let_x_be_a_meta_variable(formula_ts='Q') as q:
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=lnot(q), variables=(q,))
                    if success:
                        # The conjecture (P) is of the form (¬Q).
                        # Retrieve the value assigned to Q.
                        q_value: as1.Formula = as1.get_image_from_map(m=m, preimage=q)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            # We can safely derive ((¬Q) is-a proposition).
                            t, _ = as1.derive_1(
                                c=lnot(q_value) | is_a | proposition,
                                p=(
                                    q_value | is_a | proposition,),
                                i=i2, t=t)
                            return t, True
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                with (as1.let_x_be_a_meta_variable(formula_ts='Q') as q,
                      as1.let_x_be_a_meta_variable(formula_ts='R') as r):
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=q | land | r,
                                                                            variables=(q, r,))
                    if success:
                        # The conjecture (P) is of the form (Q ∧ R).
                        # Retrieve the values assigned to Q and R.
                        q_value: as1.Formula = as1.get_image_from_map(m=m, preimage=q)
                        r_value: as1.Formula = as1.get_image_from_map(m=m, preimage=r)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            t, success = self.process_conjecture(conjecture=r_value | is_a | proposition, t=t)
                            if success:
                                # (R is-a proposition) is proved.
                                # We can safely derive ((Q ∧ R) is-a proposition).
                                t, _ = as1.derive_1(
                                    c=(q_value | land | r_value) | is_a | proposition,
                                    p=(
                                        q_value | is_a | proposition,
                                        r_value | is_a | proposition,),
                                    i=i3, t=t)
                                return t, True
                            else:
                                # (R is-a proposition) is not proved.
                                return t, False
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                with (as1.let_x_be_a_meta_variable(formula_ts='Q') as q,
                      as1.let_x_be_a_meta_variable(formula_ts='R') as r):
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=q | implies | r,
                                                                            variables=(q, r,))
                    if success:
                        # The conjecture (P) is of the form (Q ⊃ R).
                        # Retrieve the values assigned to Q and R.
                        q_value: as1.Formula = as1.get_image_from_map(m=m, preimage=q)
                        r_value: as1.Formula = as1.get_image_from_map(m=m, preimage=r)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            t, success = self.process_conjecture(conjecture=r_value | is_a | proposition, t=t)
                            if success:
                                # (R is-a proposition) is proved.
                                # We can safely derive ((Q ⊃ R) is-a proposition).
                                t, _ = as1.derive_1(
                                    c=(q_value | implies | r_value) | is_a | proposition,
                                    p=(
                                        q_value | is_a | proposition,
                                        r_value | is_a | proposition,),
                                    i=i4, t=t)
                                return t, True
                            else:
                                # (R is-a proposition) is not proved.
                                return t, False
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                with (as1.let_x_be_a_meta_variable(formula_ts='Q') as q,
                      as1.let_x_be_a_meta_variable(formula_ts='R') as r):
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=q | lor | r,
                                                                            variables=(q, r,))
                    if success:
                        # The conjecture (P) is of the form (Q ∨ R).
                        # Retrieve the values assigned to Q and R.
                        q_value: as1.Formula = as1.get_image_from_map(m=m, preimage=q)
                        r_value: as1.Formula = as1.get_image_from_map(m=m, preimage=r)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            t, success = self.process_conjecture(conjecture=r_value | is_a | proposition, t=t)
                            if success:
                                # (R is-a proposition) is proved.
                                # We can safely derive ((Q ∨ R) is-a proposition).
                                t, _ = as1.derive_1(
                                    c=(q_value | lor | r_value) | is_a | proposition,
                                    p=(
                                        q_value | is_a | proposition,
                                        r_value | is_a | proposition,),
                                    i=i5, t=t)
                                return t, True
                            else:
                                # (R is-a proposition) is not proved.
                                return t, False
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                # The conjecture is not in any of the required forms above.
                return t, False
            else:
                # The conjecture is not of the form (P is-a proposition).
                # This heuristic is not applicable.
                return t, False


p_is_a_proposition_heuristic = PIsAProposition()
"""The (P is-a proposition) heuristic derives automatically any proposition of the form (P is-a proposition).

It is a "closed" heuristic, in the sense that it does not call general derivation heuristics recursively.
Instead, it only calls itself recursively.
"""

propositional_logic_syntax_1: as1.Theory = as1.Theory()
propositional_logic_syntax_1, _ = as1.let_x_be_an_axiom(a=i0, t=propositional_logic_syntax_1)
propositional_logic_syntax_1, _ = as1.let_x_be_an_axiom(a=i1, t=propositional_logic_syntax_1)
propositional_logic_syntax_1, _ = as1.let_x_be_an_axiom(a=i2, t=propositional_logic_syntax_1)
propositional_logic_syntax_1, _ = as1.let_x_be_an_axiom(a=i3, t=propositional_logic_syntax_1)
propositional_logic_syntax_1, _ = as1.let_x_be_an_axiom(a=i4, t=propositional_logic_syntax_1)
propositional_logic_syntax_1, _ = as1.let_x_be_an_axiom(a=i5, t=propositional_logic_syntax_1)
propositional_logic_syntax_1.heuristics.add(p_is_a_proposition_heuristic)


def extend_theory_with_propositional_logic_syntax_1(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with:
     - the propositional-logic-syntax-1 axioms,
     - the "p is-a proposition" heuristic.

    """
    global propositional_logic_syntax_1
    t = as1.append_to_theory(propositional_logic_syntax_1, t=t)
    return t
    # global i0, i1, i2, i3, i4, i5, p_is_a_proposition_heuristic
    # t: as1.Theory = as1.coerce_theory(t=t)
    # t, _ = as1.let_x_be_an_axiom(a=i0, t=t)
    # t, _ = as1.let_x_be_an_axiom(a=i1, t=t)
    # t, _ = as1.let_x_be_an_axiom(a=i2, t=t)
    # t, _ = as1.let_x_be_an_axiom(a=i3, t=t)
    # t, _ = as1.let_x_be_an_axiom(a=i4, t=t)
    # t, _ = as1.let_x_be_an_axiom(a=i5, t=t)
    # t.heuristics.add(p_is_a_proposition_heuristic)
    # return t


def let_x_be_a_propositional_logic_syntax_1_theory() -> as1.Theory:
    """Return a new theory with:
     - the propositional-logic-syntax-1 axioms,
     - the "p is-a proposition" heuristic.
     """
    t: as1.Theory = as1.Theory()
    t = extend_theory_with_propositional_logic_syntax_1(t=t)
    return t
