""""""
import punctilious as pu


class MGZ2021MinimalLogicM0(pu.Package):

    def __init__(self, u: (None, pu.UniverseOfDiscourse) = None):
        if u is None:
            u = pu.UniverseOfDiscourse()
        self.u = u
        # Naming conventions in MGZ21
        axiom_symbol = pu.StyledText(plaintext='PL', text_style=pu.text_styles.sans_serif_normal)
        theory_symbol = pu.StyledText(plaintext='M', text_style=pu.text_styles.sans_serif_normal)
        t = self.u.declare_theory(symbol=theory_symbol, index=0, dashed_name='minimal-logic',
            name='minimal logic', explicit_name='minimal logic [MGZ21]')
        self.t = t
        self.m0 = t

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
                p=((a | u.r.implies | b) | u.r.land | (b | u.r.implies | c)) | u.r.implies | (
                        a | u.r.implies | c), lock=True)

        # Axiom: PL5
        self.pl5_declaration = u.declare_axiom(symbol=axiom_symbol, index=5,
            natural_language=f'𝐵 ⊃ (𝐴 ⊃ 𝐵)')
        self.pl5_inclusion = t.include_axiom(ref='PL5', symbol=axiom_symbol, index=5,
            a=self.pl5_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl5_inclusion,
                p=b | u.r.implies | (a | u.r.implies | b), lock=True)

        # Axiom: PL6
        self.pl6_declaration = u.declare_axiom(symbol=axiom_symbol, index=6,
            natural_language=f'(𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵')
        self.pl6_inclusion = t.include_axiom(ref='PL6', symbol=axiom_symbol, index=6,
            a=self.pl6_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl6_inclusion,
                p=(a | u.r.land | (a | u.r.implies | b)) | u.r.implies | b, lock=True)

        # Axiom: PL7
        self.pl7_declaration = u.declare_axiom(symbol=axiom_symbol, index=7,
            natural_language=f'𝐴 ⊃ (𝐴 ∨ 𝐵)')
        self.pl7_inclusion = t.include_axiom(ref='PL7', symbol=axiom_symbol, index=7,
            a=self.pl7_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl7_inclusion,
                p=a | u.r.implies | (a | u.r.lor | b), lock=True)

        # Axiom: PL8
        self.pl8_declaration = u.declare_axiom(symbol=axiom_symbol, index=8,
            natural_language=f'(𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)')
        self.pl8_inclusion = t.include_axiom(ref='PL8', symbol=axiom_symbol, index=8,
            a=self.pl8_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl8_inclusion,
                p=(a | u.r.lor | b) | u.r.implies | (b | u.r.lor | a), lock=True)

        # Axiom: PL9
        self.pl9_declaration = u.declare_axiom(symbol=axiom_symbol, index=9,
            natural_language=f'[(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]')
        self.pl9_inclusion = t.include_axiom(ref='PL9', symbol=axiom_symbol, index=9,
            a=self.pl9_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b, u.v(
                symbol='C', auto_index=False) as c:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl9_inclusion,
                p=((a | u.r.implies | c) | u.r.land | (b | u.r.implies | c)) | u.r.implies | (
                        (a | u.r.lor | b) | u.r.implies | c), lock=True)

        # Axiom: PL10
        self.pl10_declaration = u.declare_axiom(symbol=axiom_symbol, index=10,
            natural_language=f'[(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴')
        self.pl10_inclusion = t.include_axiom(ref='PL10', symbol=axiom_symbol, index=10,
            a=self.pl10_declaration)
        with u.v(symbol='A', auto_index=False) as a, u.v(symbol='B', auto_index=False) as b:
            t.i.axiom_interpretation.infer_formula_statement(a=self.pl10_inclusion, p=((
                                                                                               a | u.r.implies | b) | u.r.land | (
                                                                                               a | u.r.implies | u.r.lnot(
                                                                                           b))) | u.r.implies | u.r.lnot(
                a), lock=True)
