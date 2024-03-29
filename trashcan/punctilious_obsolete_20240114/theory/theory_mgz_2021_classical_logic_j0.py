""""""
import punctilious as pu
from theory.theory_mgz_2021_intuitionistic_logic_j0 import MGZ2021IntuitionisticLogicJ0


class MGZ2021ClassicalLogicK0(pu.TheoryPackage):

    def __init__(self, u: (None, pu.UniverseOfDiscourse) = None):
        super().__init__()
        if u is None:
            u = pu.UniverseOfDiscourse()
        self.u = u

        # Naming conventions in MGZ21
        axiom_symbol = pu.StyledText(plaintext='PL', text_style=pu.text_styles.sans_serif_normal)
        theory_symbol = pu.StyledText(plaintext='K', text_style=pu.text_styles.sans_serif_normal)
        self.j0_package = MGZ2021IntuitionisticLogicJ0(u=u)
        t = self.u.t.register(symbol=theory_symbol, index=0, dashed_name='classical-logic', name='classical logic',
            explicit_name='classical logic [MGZ21]', extended_theory=self.j0_package.j0)
        self.t = t
        self.m0 = self.j0_package.m0
        self.j0 = self.j0_package.j0
        self.k0 = t

        section_1 = t.open_section(section_title='Classical Logic', section_number=1)

        # Axiom: PL12
        self.pl12_declaration = u.a.register(symbol=axiom_symbol, index=12, natural_language=f'¬¬𝐴 ⊃ 𝐴')
        self.pl12_inclusion = t.include_axiom(ref='PL12', symbol=axiom_symbol, index=1, a=self.pl12_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B', auto_index=False) as b:
            self.pl12_statement = t.i.axiom_interpretation.infer_formula_statement(a=self.pl12_inclusion,
                p=u.c1.lnot(u.c1.lnot(a)) | u.c1.implies | a, lock=True)
