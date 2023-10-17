""""""
import punctilious as pu


class Mancosou2021MinimalLogicM0(pu.Package):

    def __init__(self, t: (None, pu.TheoryElaborationSequence) = None,
            u: (None, pu.UniverseOfDiscourse) = None):

        # Naming conventions in Mancosou 2021
        axiom_symbol = pu.StyledText(plaintext='PL', text_style=pu.text_styles.sans_serif_normal)
        theory_symbol = pu.StyledText(plaintext='M', text_style=pu.text_styles.sans_serif_normal)
        self.u = u
        self.t = t
        if self.u is None and self.t is None:
            self.u = pu.UniverseOfDiscourse()
            self.t = self.u.declare_theory(symbol=theory_symbol, index=0)
        elif self.u is None and self.t is not None:
            self.u = self.t.u
        elif self.u is not None and self.t is None:
            self.t = self.u.declare_theory(symbol=theory_symbol, index=0)
        u = self.u
        t = self.t
        section_1 = t.open_section(section_title='Minimal Logic', section_number=1)

        # Axiom: PL1
        self.pl1_declaration = u.declare_axiom(symbol=axiom_symbol, index=1,
            natural_language=f'𝐴 ⊃ (𝐴 ∧ 𝐴)')
        self.pl1_inclusion = t.include_axiom(ref='PL1', symbol=axiom_symbol, index=1,
            a=self.pl1_declaration)
        with u.v(symbol='A', auto_index=False) as a:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl1_inclusion,
                p=a | u.r.implies | (a | u.r.land | a), lock=True)

        # Axiom: PL2
        self.pl2_declaration = u.declare_axiom(symbol=axiom_symbol, index=2,
            natural_language=f'(𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)')
        self.pl2_inclusion = t.include_axiom(ref='PL2', symbol=axiom_symbol, index=2,
            a=self.pl2_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl2_inclusion,
                p=(a | u.r.land | b) | u.r.implies | (b | u.r.land | a), lock=True)

        # Axiom: PL3
        self.pl3_declaration = u.declare_axiom(symbol=axiom_symbol, index=3,
            natural_language=f'(𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]')
        self.pl3_inclusion = t.include_axiom(ref='PL3', symbol=axiom_symbol, index=3,
            a=self.pl3_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b, u.v(
                symbol='C', auto_index=False) as c:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl3_inclusion,
                p=(a | u.r.implies | b) | u.r.implies | (
                        (a | u.r.land | c) | u.r.implies | (b | u.r.land | c)), lock=True)

        # Axiom: PL4
        self.pl4_declaration = u.declare_axiom(symbol=axiom_symbol, index=4,
            natural_language=f'[(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)')
        self.pl4_inclusion = t.include_axiom(ref='PL4', symbol=axiom_symbol, index=4,
            a=self.pl4_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b, u.v(
                symbol='C', auto_index=False) as c:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl4_inclusion,
                p=((a | u.r.land | c) | u.r.implies | (b | u.r.land | c)) | u.r.implies | (
                        a | u.r.implies | b), lock=True)

        # Axiom: PL5
        self.pl5_declaration = u.declare_axiom(symbol=axiom_symbol, index=5,
            natural_language=f'𝐵 ⊃ (𝐴 ⊃ 𝐵)')
        self.pl5_inclusion = t.include_axiom(ref='PL5', symbol=axiom_symbol, index=5,
            a=self.pl5_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl5_inclusion,
                p=b | u.r.implies | (a | u.r.implies | b), lock=True)


test = Mancosou2021MinimalLogicM0()
