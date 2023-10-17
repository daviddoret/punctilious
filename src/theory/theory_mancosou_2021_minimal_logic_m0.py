""""""
import punctilious as pu


class Mancosou2021MinimalLogicM0(pu.Package):

    def __init__(self, t: (None, pu.TheoryElaborationSequence) = None,
            u: (None, pu.UniverseOfDiscourse) = None):

        # Naming conventions in Mancosou 2021
        axiom_symbol = pu.StyledText(plaintext='PL', text_style=pu.text_styles.sans_serif_normal)

        self.u = u
        self.t = t
        if self.u is None and self.t is None:
            self.u = pu.UniverseOfDiscourse()
            self.t = self.u.declare_theory(
                symbol=pu.StyledText(plaintext='M', text_style=pu.text_styles.sans_serif_normal),
                index=0)
        elif self.u is None and self.t is not None:
            self.u = self.t.u
        elif self.u is not None and self.t is None:
            self.t = self.u.declare_theory(
                symbol=pu.StyledText(plaintext='M', text_style=pu.text_styles.sans_serif_normal),
                index=0)
        u = self.u
        t = self.t
        section_2 = t.open_section('Minimal Logic', section_number=2)

        self.pl1 = u.declare_axiom(ref='PL1', symbol=axiom_symbol, index=1,
            natural_language=f'𝐴 ⊃ (𝐴 ∧ 𝐴)')
        inclusion = t.include_axiom(ref='PL1', symbol=axiom_symbol, index=1, a=self.pl1)
        with u.v(symbol='A', auto_index=False) as a:
            t.i.axiom_interpretation.infer_formula_statement(a=inclusion,
                p=a | u.r.implies | (a | u.r.land | a))  # inclusion.lock_axiom()


test = Mancosou2021MinimalLogicM0()
