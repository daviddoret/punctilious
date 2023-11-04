""""""
from __future__ import annotations

import contextlib
import punctilious as pu
from punctilious.core import FlexibleFormula


class MGZ2021PropositionalLogic(pu.TheoryPackage):

    def __init__(self, u: (None, pu.UniverseOfDiscourse) = None):
        if u is None:
            u = pu.UniverseOfDiscourse()
        super().__init__(u=u)
        self._l = Language(theory_package=self)
        # Naming conventions in MGZ21
        theory_symbol = pu.StyledText(plaintext='L', text_style=pu.text_styles.script_normal)
        t = self.u.declare_theory(symbol=theory_symbol, index=1, dashed_name='propositional-logic',
            name='propositional logic', explicit_name='propositional logic [MGZ21]')
        self.t = t
        self.l1 = t

        # meta-theory
        metatheory = self.u.declare_theory(symbol=theory_symbol, index=1,
            dashed_name='meta-propositional-logic', name='meta propositional logic')
        self.metatheory = metatheory

        section_2 = t.open_section(section_title='Axiomatic Calculi', section_number=2)
        section_2_1 = t.open_section(section_parent=section_2, section_title='Propositional Logic',
            section_number=1)

        # Definition 2.1
        def_2_1_declaration = u.declare_axiom(natural_language="""The language of 
        propositional logic consists of:
        1. A denumerable set of propositional variables 𝑝1, 𝑝2, 𝑝3, ...
        2. Connectives: ¬, ∨, ∧, ⊃
        3. Parenthesis: (,)""")
        self.def_2_1_declaration = def_2_1_declaration
        def_2_1_inclusion = t.include_axiom(ref='2.1', index=1, a=self.def_2_1_declaration)
        self.def_2_1_inclusion = def_2_1_inclusion

        self.is_a = u.r.is_a
        is_a = self.is_a
        self.propositional_variable = u.c2.declare(symbol='propositional-variable',
            auto_index=False)
        self.lnot = u.r.lnot
        self.lor = u.r.lor
        self.land = u.r.land
        self.implies = u.r.implies
        propositional_variable = self.propositional_variable
        lnot = self.lnot
        lor = self.lor
        land = self.land
        implies = self.implies

        # Definition 2.2
        self.def_2_2_declaration = u.declare_axiom(natural_language="""The formulas are defined as 
        follows: 
        1. Basis clause: Each propositional variable is a formula (called an atomic formula). 
        2. Inductive clause: If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵). 
        3. Extremal clause: Nothing else is a formula.""")
        self.def_2_2_inclusion = t.include_axiom(ref='2.2', index=1, a=self.def_2_2_declaration)

        self.propositional_formula = u.c2.declare(symbol='propositional-formula', auto_index=False)
        propositional_formula = self.propositional_formula
        with u.with_variable(symbol='p') as p:
            t.i.axiom_interpretation.infer_formula_statement(a=self.def_2_1_inclusion,
                p=(p | is_a | propositional_variable) | implies | (
                        p | is_a | propositional_formula))  # t.i.modus_ponens.infer_formula_statement(a=self.def_2_2_inclusion,  #    p=(p | is_a | propositional_variable) | implies | (  #            p | is_a | propositional_formula))

    @property
    def l(self) -> Language:
        return self._l


class Language(pu.CollectionDeclaration):
    """The language of propositional logic."""

    def __init__(self, theory_package: pu.TheoryPackage):
        self._theory_package = theory_package
        self._u = theory_package.u
        symbol = pu.StyledText(plaintext='L', text_style=pu.text_styles.script_normal)
        self._propositional_variable_symbol = pu.StyledText(plaintext='p',
            text_style=pu.text_styles.sans_serif_normal)
        super().__init__(u=self._u, symbol=symbol)
        self.lnot = self._u.r.lnot
        self.lor = self._u.r.lor
        self.land = self._u.r.land
        self.implies = self._u.r.implies

    @contextlib.contextmanager
    def with_propositional_variable(self, echo: (None, bool) = None):
        """Yield a new propositional-variable.

        :param symbol:
        :param index:
        :param auto_index:
        :param echo:
        :return:
        """
        with self.u.with_variable(symbol=self._propositional_variable_symbol, index=None,
                auto_index=True, echo=echo) as p:
            # Extend the language collection to include this new propositional-variable.
            self._extend(phi=p)
            yield p

    def _extend(self, phi: FlexibleFormula) -> None:
        """This private method extends the language collection in an authorized manner."""
        super().extend(phi=phi)

    def extend(self, phi: FlexibleFormula) -> None:
        """Manually extending the propositional-language collection is forbidden. In effect,
        the extremal clause of the language definition prevents any object that is not defined in the first and second clause.
        TODO: Provide reference to MGZ definition 2.1 and 2.2.
        use the with_propositional_variable() method to declare new propositional variables.
        """
        raise pu.PunctiliousException("")


x = MGZ2021PropositionalLogic()
with x.l.with_propositional_variable(echo=True) as pa:
    print('hello')
