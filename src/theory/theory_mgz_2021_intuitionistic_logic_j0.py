""""""
import punctilious as pu
from theory.theory_mgz_2021_minimal_logic_m0 import MGZ2021MinimalLogicM0


class MGZ2021IntuitionisticLogicJ0(pu.TheoryPackage):

    def __init__(self, u: (None, pu.UniverseOfDiscourse) = None):
        super().__init__()
        if u is None:
            u = pu.UniverseOfDiscourse()
        self.u = u

        # Naming conventions in MGZ21
        axiom_symbol = pu.StyledText(plaintext='PL', text_style=pu.text_styles.sans_serif_normal)
        theory_symbol = pu.StyledText(plaintext='J', text_style=pu.text_styles.sans_serif_normal)
        self.m0_package = MGZ2021MinimalLogicM0(u=u)
        t = self.u.declare_theory(symbol=theory_symbol, index=0, dashed_name='intuitionistic-logic',
            name='intuitionistic logic', explicit_name='intuitionistic logic [MGZ21]',
            extended_theory=self.m0_package.m0)
        self.t = t
        self.m0 = self.m0_package.m0
        self.j0 = t

        section_1 = t.open_section(section_title='Intuitionistic Logic', section_number=1)

        # Axiom: PL11
        self.pl11_declaration = u.declare_axiom(symbol=axiom_symbol, index=11, natural_language=f'¬𝐴 ⊃ (𝐴 ⊃ 𝐵)')
        self.pl11_inclusion = t.include_axiom(ref='PL11', symbol=axiom_symbol, index=1, a=self.pl11_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B', auto_index=False) as b:
            self.pl11_statement = t.i.axiom_interpretation.infer_formula_statement(a=self.pl11_inclusion,
                p=u.c1.lnot(a) | u.c1.implies | (a | u.c1.implies | b), lock=True)
