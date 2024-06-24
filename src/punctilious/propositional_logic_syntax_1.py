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

with as1.let_x_be_a_variable(formula_typesetter='A') as a, as1.let_x_be_a_variable(formula_typesetter='B') as b:
    i6: as1.InferenceRule = as1.InferenceRule(
        transformation=as1.Transformation(
            premises=None,
            conclusion=lnot(a | is_a | proposition),
            variables=(a, b,)))
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

axiomatization = as1.Axiomatization(derivations=(i1, i2, i3, i4, i5,))

extended_theory = as1.Theory(derivations=(*axiomatization,))


def let_x_be_a_propositional_variable(
        t: as1.FlexibleTheory,
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

    :param t:
    :param rep:
    :return:
    """
    global axiomatization
    global i1
    t: as1.FlexibleTheory = as1.coerce_theory(phi=t)

    # Include all propositional-logic-syntax-1 axioms if they are not already present
    # in the theory.
    t = as1.extend_theory(axiomatization, t=t)

    if isinstance(rep, str):
        # declare a single propositional variable
        x = as1.Variable(connective=as1.NullaryConnective(formula_typesetter=rep))
        t, _ = as1.let_x_be_an_axiom(t=t,
                                     valid_statement=x | as1.connectives.is_a | as1.connectives.propositional_variable)

        return t, x
    elif isinstance(rep, typing.Iterable):
        # declare multiple propositional variables
        propositional_variables = tuple()
        for r in rep:
            x = as1.Variable(connective=as1.NullaryConnective(formula_typesetter=r))
            propositional_variables = propositional_variables + (x,)
            t, _ = as1.let_x_be_an_axiom(t=t,
                                         valid_statement=x | as1.connectives.is_a | as1.connectives.propositional_variable)
            t, _ = as1.derive_1(t=t,
                                conjecture=x | is_a | proposition,
                                premises=(x | as1.connectives.is_a | as1.connectives.propositional_variable,),
                                inference_rule=i1)
        return t, *propositional_variables
    else:
        raise TypeError  # TODO: Implement event code.


class PIsAProposition(as1.Heuristic):

    def process_conjecture(self, conjecture: as1.FlexibleFormula, t: as1.FlexibleTheory) -> tuple[as1.Theory, bool,]:
        conjecture: as1.Formula = as1.coerce_formula(phi=conjecture)
        t: as1.Theory = as1.coerce_theory(phi=t)

        t, success, _ = as1.derive_0(conjecture=conjecture, t=t)
        if success:
            # The conjecture is already proven in the theory.
            return t, True

        with as1.let_x_be_a_meta_variable(formula_typesetter='P') as p:
            success, m = as1.is_formula_equivalent_with_variables_2(
                phi=conjecture, psi=p | is_a | proposition, variables=(p,))

            if success:
                # The conjecture is of the form (P is-a proposition).
                # Make an attempt to automatically derive the conjecture.

                # retrieve P's value
                p_value: as1.Formula = m.get_assigned_value(phi=p)

                if as1.is_valid_statement_in_theory(phi=p_value | is_a | propositional_variable, t=t):
                    # If P is a propositional-variable:
                    # We can safely derive p | is_a | proposition
                    t, _ = as1.derive_1(
                        conjecture=p_value | is_a | proposition,
                        premises=(
                            p_value | is_a | propositional_variable,),
                        inference_rule=i1, t=t)

                    return t, True

                with as1.let_x_be_a_meta_variable(formula_typesetter='Q') as q:
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=lnot(q), variables=(q,))
                    if success:
                        # The conjecture (P) is of the form (¬Q).
                        # Retrieve the value assigned to Q.
                        q_value: as1.Formula = m.get_assigned_value(phi=q)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            # We can safely derive ((¬Q) is-a proposition).
                            t, _ = as1.derive_1(
                                conjecture=lnot(q_value) | is_a | proposition,
                                premises=(
                                    q_value | is_a | proposition,),
                                inference_rule=i2, t=t)
                            return t, True
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                with (as1.let_x_be_a_meta_variable(formula_typesetter='Q') as q,
                      as1.let_x_be_a_meta_variable(formula_typesetter='R') as r):
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=q | land | r,
                                                                            variables=(q, r,))
                    if success:
                        # The conjecture (P) is of the form (Q ∧ R).
                        # Retrieve the values assigned to Q and R.
                        q_value: as1.Formula = m.get_assigned_value(phi=q)
                        r_value: as1.Formula = m.get_assigned_value(phi=r)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            t, success = self.process_conjecture(conjecture=r_value | is_a | proposition, t=t)
                            if success:
                                # (R is-a proposition) is proved.
                                # We can safely derive ((Q ∧ R) is-a proposition).
                                t, _ = as1.derive_1(
                                    conjecture=(q_value | land | r_value) | is_a | proposition,
                                    premises=(
                                        q_value | is_a | proposition,
                                        r_value | is_a | proposition,),
                                    inference_rule=i3, t=t)
                                return t, True
                            else:
                                # (R is-a proposition) is not proved.
                                return t, False
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                with (as1.let_x_be_a_meta_variable(formula_typesetter='Q') as q,
                      as1.let_x_be_a_meta_variable(formula_typesetter='R') as r):
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=q | implies | r,
                                                                            variables=(q, r,))
                    if success:
                        # The conjecture (P) is of the form (Q ⊃ R).
                        # Retrieve the values assigned to Q and R.
                        q_value: as1.Formula = m.get_assigned_value(phi=q)
                        r_value: as1.Formula = m.get_assigned_value(phi=r)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            t, success = self.process_conjecture(conjecture=r_value | is_a | proposition, t=t)
                            if success:
                                # (R is-a proposition) is proved.
                                # We can safely derive ((Q ⊃ R) is-a proposition).
                                t, _ = as1.derive_1(
                                    conjecture=(q_value | implies | r_value) | is_a | proposition,
                                    premises=(
                                        q_value | is_a | proposition,
                                        r_value | is_a | proposition,),
                                    inference_rule=i4, t=t)
                                return t, True
                            else:
                                # (R is-a proposition) is not proved.
                                return t, False
                        else:
                            # (Q is-a proposition) is not proved.
                            return t, False

                with (as1.let_x_be_a_meta_variable(formula_typesetter='Q') as q,
                      as1.let_x_be_a_meta_variable(formula_typesetter='R') as r):
                    success, m = as1.is_formula_equivalent_with_variables_2(phi=p_value, psi=q | lor | r,
                                                                            variables=(q, r,))
                    if success:
                        # The conjecture (P) is of the form (Q ∨ R).
                        # Retrieve the values assigned to Q and R.
                        q_value: as1.Formula = m.get_assigned_value(phi=q)
                        r_value: as1.Formula = m.get_assigned_value(phi=r)
                        # Recursively try to derive (Q is-a proposition).
                        t, success = self.process_conjecture(conjecture=q_value | is_a | proposition, t=t)
                        if success:
                            # (Q is-a proposition) is proved.
                            t, success = self.process_conjecture(conjecture=r_value | is_a | proposition, t=t)
                            if success:
                                # (R is-a proposition) is proved.
                                # We can safely derive ((Q ∨ R) is-a proposition).
                                t, _ = as1.derive_1(
                                    conjecture=(q_value | lor | r_value) | is_a | proposition,
                                    premises=(
                                        q_value | is_a | proposition,
                                        r_value | is_a | proposition,),
                                    inference_rule=i5, t=t)
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


def extend_theory_with_propositional_logic_syntax_1(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with:
     - the propositional-logic-syntax-1 axioms,
     - the "p is-a proposition" heuristic.

    """
    global i1, i2, i3, i4, i5, p_is_a_proposition_heuristic
    t: as1.Theory = as1.coerce_theory(phi=t)
    t, _ = as1.let_x_be_an_axiom(axiom=i1, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=i2, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=i3, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=i4, t=t)
    t, _ = as1.let_x_be_an_axiom(axiom=i5, t=t)
    t.heuristics.add(p_is_a_proposition_heuristic)
    return t


def let_x_be_a_propositional_logic_syntax_1_theory() -> as1.Theory:
    """Return a new theory with:
     - the propositional-logic-syntax-1 axioms,
     - the "p is-a proposition" heuristic.
     """
    t: as1.Theory = as1.Theory()
    t = extend_theory_with_propositional_logic_syntax_1(t=t)
    return t
