""""""
from __future__ import annotations

import contextlib
import punctilious as pu
from punctilious.core import FlexibleFormula


class ErrorCodes:
    # TODO: Extend the system error codes instead of declaring a new class?
    def __init__(self):
        self.error_101_invalid_propositional_formula_components = pu.ErrorCode(101, 'Invalid propositional formula '
                                                                                    'components')


error_codes = ErrorCodes()


class MGZ2021PropositionalLogic(pu.TheoryPackage):

    def __init__(self, u: (None, pu.UniverseOfDiscourse) = None):
        if u is None:
            u = pu.UniverseOfDiscourse()
        super().__init__(u=u)

        # Naming conventions in MGZ21
        self._formula_symbol = pu.StyledText(plaintext='phi', unicode='𝜑', latex=r'\phi',
            text_style=pu.text_styles.serif_italic)
        self._propositional_variable_symbol = pu.StyledText(plaintext='p', text_style=pu.text_styles.serif_italic)

        # meta-theory
        metatheory: pu.TheoryDerivation = self.u.declare_theory(
            symbol=pu.StyledText(plaintext='PLM', text_style=pu.text_styles.script_normal), index=None,
            auto_index=False, dashed_name='propositional-logic-metatheory', name='propositional logic metatheory')
        self._metatheory = metatheory

        section_2 = metatheory.open_section(section_title='Axiomatic Calculi', section_number=2)
        section_2_1 = metatheory.open_section(section_parent=section_2, section_title='Propositional Logic',
            section_number=1)

        # Definition 2.1
        def_2_1_declaration = u.a.declare(natural_language="""The language of 
        propositional logic consists of:
        1. A denumerable set of propositional variables 𝑝1, 𝑝2, 𝑝3, ...
        2. Connectives: ¬, ∨, ∧, ⊃
        3. Parenthesis: (,)""")
        self.def_2_1_declaration = def_2_1_declaration
        def_2_1 = metatheory.include_axiom(ref='2.1', index=1, a=self.def_2_1_declaration)
        self.def_2_1 = def_2_1
        metatheory.take_note(subtitle='Regarding parenthesis in definition 2.1',
            content='Punctilious models compound-formulas as trees. It follows '
                    'that parenthesis are not needed as objects of the theory, '
                    'but parenthesis are automatically displayed when formulae '
                    'are composed.')

        # Declares the propositional-connective class
        propositional_connective = u.c2.declare(symbol='propositional-connective', auto_index=False)
        self.propositional_connective: pu.ClassDeclaration = propositional_connective

        is_a: pu.Connective = u.c1.is_a
        self.is_a = is_a
        object_reference: pu.Connective = u.c1.object_reference
        self.object_reference = object_reference

        # Add all members to the propositional-connective class
        self.lnot: pu.Connective = u.c1.lnot
        self.lor: pu.Connective = u.c1.lor
        self.land: pu.Connective = u.c1.land
        self.implies: pu.Connective = u.c1.implies
        lnot: pu.Connective = self.lnot
        lor: pu.Connective = self.lor
        land: pu.Connective = self.land
        implies: pu.Connective = self.implies
        metatheory.i.axiom_interpretation.infer_formula_statement(a=def_2_1, p=lnot | is_a | propositional_connective,
            lock=False)
        metatheory.i.axiom_interpretation.infer_formula_statement(a=def_2_1, p=lor | is_a | propositional_connective,
            lock=False)
        metatheory.i.axiom_interpretation.infer_formula_statement(a=def_2_1, p=land | is_a | propositional_connective,
            lock=False)
        metatheory.i.axiom_interpretation.infer_formula_statement(a=def_2_1,
            p=implies | is_a | propositional_connective, lock=False)
        # TODO: We should find a way here to "lock" the propositional-connective class because we
        #  have defined all of its members. We want to prevent any accidental addition of another
        #  connective. One possibility would be to postulate a statement saying that if an object
        #  is a propositional-connective and is not one of the above, then the theory is
        #  inconsistent. But this should be analysed further.

        self.propositional_variable: pu.ClassDeclaration = u.c2.declare(symbol='propositional-variable',
            auto_index=False)
        propositional_variable: pu.ClassDeclaration = self.propositional_variable

        # Definition 2.2
        self.def_2_2_declaration = u.a.declare(natural_language="""The formulas are defined as 
        follows: 
        1. Basis clause: Each propositional variable is a formula (called an atomic formula). 
        2. Inductive clause: If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵). 
        3. Extremal clause: Nothing else is a formula.""")
        def_2_2 = metatheory.include_axiom(ref='2.2', index=1, a=self.def_2_2_declaration)
        self.def_2_2 = def_2_2

        self.propositional_formula: pu.ClassDeclaration = u.c2.declare(symbol='propositional-formula', auto_index=False)
        propositional_formula: pu.ClassDeclaration = self.propositional_formula

        with u.with_variable(symbol='A') as a:
            self.meta_10 = metatheory.i.axiom_interpretation.infer_formula_statement(lock=False, a=def_2_2,
                p=(a | is_a | propositional_variable) | implies | (a | is_a | propositional_formula))
        with u.with_variable(symbol='A') as a:
            self.meta_11 = metatheory.i.axiom_interpretation.infer_formula_statement(lock=False, a=def_2_2,
                p=(a | is_a | propositional_formula) | implies | (lnot(a) | is_a | propositional_formula))
        with u.with_variable(symbol='A') as a, u.with_variable(symbol='B') as b:
            self.meta_12 = metatheory.i.axiom_interpretation.infer_formula_statement(lock=False, a=def_2_2,
                p=((a | is_a | propositional_formula) | land | (b | is_a | propositional_formula)) | implies | (
                    (a | lor | b) | is_a | propositional_formula))
        with u.with_variable(symbol='A') as a, u.with_variable(symbol='B') as b:
            self.meta_13 = metatheory.i.axiom_interpretation.infer_formula_statement(lock=False, a=def_2_2,
                p=((a | is_a | propositional_formula) | land | (b | is_a | propositional_formula)) | implies | (
                    (a | land | b) | is_a | propositional_formula))
        with u.with_variable(symbol='A') as a, u.with_variable(symbol='B') as b:
            self.meta_14 = metatheory.i.axiom_interpretation.infer_formula_statement(lock=True, a=def_2_2,
                p=((a | is_a | propositional_formula) | land | (b | is_a | propositional_formula)) | implies | (
                    (a | implies | b) | is_a | propositional_formula))

        # Declare the propositional-logic theory
        t = self.u.declare_theory(symbol=pu.StyledText(plaintext='L', text_style=pu.text_styles.script_normal), index=1,
            dashed_name='propositional-logic', name='propositional logic', explicit_name='propositional logic [MGZ21]')
        self.t = t
        self.l1 = t

    def declare_compound_formula(self, connective: pu.Connective, *terms, lock_variable_scope: (None, bool) = None,
        echo: (None, bool) = None):
        """Declare a new formula in this universe-of-discourse.

        This method is a shortcut for Formula(universe_of_discourse=self, . . d.).

        A formula is *declared* in a theory, and not *stated*, because it is not a statement,
        i.e. it is not necessarily true in this theory.
        """
        pu.verify_formula_statement(t=self.metatheory,
            input_value=connective | self.is_a | self.propositional_connective, arg='connective',
            error_code=error_codes.error_101_invalid_propositional_formula_components)
        for term in terms:
            # We intend to make a meta statement about this variable.
            # Note that the scope of the variable is closed, prohibiting its usage in formulas.
            # But here we don't use the formula, we reference it.
            # To solve this difficulty we use the object-reference connective.
            pu.verify_formula_statement(t=self.metatheory,
                input_value=self.object_reference(term) | self.is_a | self.propositional_formula, arg='term',
                error_code=error_codes.error_101_invalid_propositional_formula_components)
        phi = pu.CompoundFormula(connective=connective, terms=terms, u=self.u, symbol=self._formula_symbol,
            lock_variable_scope=lock_variable_scope, echo=echo)
        match connective:
            case self.lnot:
                # phi := lnot(psi)
                psi = terms[0]
                psi_reference = self.object_reference(psi)
                # self.meta_11:
                # (a | is_a | propositional_formula) | implies | (lnot(a) | is_a | propositional_formula))
                p_implies_q = self.metatheory.i.variable_substitution.infer_formula_statement(p=self.meta_11,
                    phi=self.u.c1.tupl(psi_reference))
                p = psi_reference | self.is_a | self.propositional_formula
                self.metatheory.i.modus_ponens.infer_formula_statement(p_implies_q=p_implies_q, p=p)
            case self.lor:
                p2 = self.object_reference(terms[0]) | self.is_a | self.propositional_formula
                q2 = self.object_reference(terms[1]) | self.is_a | self.propositional_formula
                p3 = self.metatheory.i.conjunction_introduction.infer_formula_statement(p=p2, q=q2)
                self.metatheory.i.modus_ponens.infer_formula_statement(p_implies_q=self.meta_12, p=p3)
            case self.land:
                p2 = self.object_reference(terms[0]) | self.is_a | self.propositional_formula
                q2 = self.object_reference(terms[1]) | self.is_a | self.propositional_formula
                p3 = self.metatheory.i.conjunction_introduction.infer_formula_statement(p=p2, q=q2)
                self.metatheory.i.modus_ponens.infer_formula_statement(p_implies_q=self.meta_13, p=p3)
            case self.implies:
                p2 = self.object_reference(terms[0]) | self.is_a | self.propositional_formula
                q2 = self.object_reference(terms[1]) | self.is_a | self.propositional_formula
                p3 = self.metatheory.i.conjunction_introduction.infer_formula_statement(p=p2, q=q2)
                self.metatheory.i.modus_ponens.infer_formula_statement(p_implies_q=self.meta_14, p=p3)
        return phi

    @property
    def metatheory(self) -> pu.TheoryDerivation:
        return self._metatheory

    @contextlib.contextmanager
    def with_propositional_variable(self, echo: (None, bool) = None):
        """Declare and yield a new propositional-variable.

        :param symbol:
        :param index:
        :param auto_index:
        :param echo:
        :return:
        """
        with self.u.with_variable(symbol=self._propositional_variable_symbol, index=None, auto_index=True,
            echo=echo) as p:
            # Extend the language collection to include this new propositional-variable.
            p1 = self.metatheory.i.axiom_interpretation.infer_formula_statement(lock=False, a=self.def_2_1,
                p=self.object_reference(p) | self.is_a | self.propositional_variable)
            p_implies_q = self.metatheory.i.variable_substitution.infer_formula_statement(p=self.meta_10,
                phi=self.u.c1.tupl(self.object_reference(p)))
            self.metatheory.i.modus_ponens.infer_formula_statement(p_implies_q=p_implies_q, p=p1)
            yield p


x = MGZ2021PropositionalLogic()
with x.with_propositional_variable(echo=True) as pa:
    x.declare_compound_formula(x.lnot, pa)
    print('hello')
