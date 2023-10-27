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

        section_1_1 = t.open_section(section_title='Axioms', section_number=1,
            section_parent=section_1)

        # Axiom: PL1
        self.pl1_declaration = u.declare_axiom(symbol=axiom_symbol, index=1,
            natural_language=f'𝐴 ⊃ (𝐴 ∧ 𝐴)')
        self.pl1_inclusion = t.include_axiom(ref='PL1', symbol=axiom_symbol, index=1,
            a=self.pl1_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a:
            self.pl1_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl1_inclusion, p=a | u.r.implies | (a | u.r.land | a), lock=True)

        # Axiom: PL2
        self.pl2_declaration = u.declare_axiom(symbol=axiom_symbol, index=2,
            natural_language=f'(𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)')
        self.pl2_inclusion = t.include_axiom(ref='PL2', symbol=axiom_symbol, index=2,
            a=self.pl2_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b:
            self.pl2_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl2_inclusion, p=(a | u.r.land | b) | u.r.implies | (b | u.r.land | a),
                lock=True)

        # Axiom: PL3
        self.pl3_declaration = u.declare_axiom(symbol=axiom_symbol, index=3,
            natural_language=f'(𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]')
        self.pl3_inclusion = t.include_axiom(ref='PL3', symbol=axiom_symbol, index=3,
            a=self.pl3_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b, u.with_variable(symbol='C', auto_index=False) as c:
            self.pl3_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl3_inclusion, p=(a | u.r.implies | b) | u.r.implies | (
                        (a | u.r.land | c) | u.r.implies | (b | u.r.land | c)), lock=True)

        # Axiom: PL4
        self.pl4_declaration = u.declare_axiom(symbol=axiom_symbol, index=4,
            natural_language=f'[(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)')
        self.pl4_inclusion = t.include_axiom(ref='PL4', symbol=axiom_symbol, index=4,
            a=self.pl4_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b, u.with_variable(symbol='C', auto_index=False) as c:
            self.pl4_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl4_inclusion,
                p=((a | u.r.implies | b) | u.r.land | (b | u.r.implies | c)) | u.r.implies | (
                        a | u.r.implies | c), lock=True)

        # Axiom: PL5
        # Original: 𝐵 ⊃ (𝐴 ⊃ 𝐵)
        # Punctilious: 𝐁 ⟹ (𝐀 ⟹ 𝐁)
        self.pl5_declaration = u.declare_axiom(symbol=axiom_symbol, index=5,
            natural_language=f'𝐵 ⊃ (𝐴 ⊃ 𝐵)')
        self.pl5_inclusion = t.include_axiom(ref='PL5', symbol=axiom_symbol, index=5,
            a=self.pl5_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b:
            self.pl5_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl5_inclusion, p=b | u.r.implies | (a | u.r.implies | b), lock=True)

        # Axiom: PL6
        self.pl6_declaration = u.declare_axiom(symbol=axiom_symbol, index=6,
            natural_language=f'(𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵')
        self.pl6_inclusion = t.include_axiom(ref='PL6', symbol=axiom_symbol, index=6,
            a=self.pl6_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b:
            self.pl6_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl6_inclusion, p=(a | u.r.land | (a | u.r.implies | b)) | u.r.implies | b,
                lock=True)

        # Axiom: PL7
        self.pl7_declaration = u.declare_axiom(symbol=axiom_symbol, index=7,
            natural_language=f'𝐴 ⊃ (𝐴 ∨ 𝐵)')
        self.pl7_inclusion = t.include_axiom(ref='PL7', symbol=axiom_symbol, index=7,
            a=self.pl7_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b:
            self.pl7_statement = t.i.axiom_interpretation.infer_formula_statement(ref='PL7',
                a=self.pl7_inclusion, p=a | u.r.implies | (a | u.r.lor | b), lock=True)

        # Axiom: PL8
        self.pl8_declaration = u.declare_axiom(symbol=axiom_symbol, index=8,
            natural_language=f'(𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)')
        self.pl8_inclusion = t.include_axiom(ref='PL8', symbol=axiom_symbol, index=8,
            a=self.pl8_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b:
            self.pl8_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl8_inclusion, p=(a | u.r.lor | b) | u.r.implies | (b | u.r.lor | a),
                lock=True)

        # Axiom: PL9
        self.pl9_declaration = u.declare_axiom(symbol=axiom_symbol, index=9,
            natural_language=f'[(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]')
        self.pl9_inclusion = t.include_axiom(ref='PL9', symbol=axiom_symbol, index=9,
            a=self.pl9_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b, u.with_variable(symbol='C', auto_index=False) as c:
            self.pl9_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl9_inclusion,
                p=((a | u.r.implies | c) | u.r.land | (b | u.r.implies | c)) | u.r.implies | (
                        (a | u.r.lor | b) | u.r.implies | c), lock=True)

        # Axiom: PL10
        self.pl10_declaration = u.declare_axiom(symbol=axiom_symbol, index=10,
            natural_language=f'[(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴')
        self.pl10_inclusion = t.include_axiom(ref='PL10', symbol=axiom_symbol, index=10,
            a=self.pl10_declaration)
        with u.with_variable(symbol='A', auto_index=False) as a, u.with_variable(symbol='B',
                auto_index=False) as b:
            self.pl10_statement = t.i.axiom_interpretation.infer_formula_statement(
                a=self.pl10_inclusion, p=((a | u.r.implies | b) | u.r.land | (
                        a | u.r.implies | u.r.lnot(b))) | u.r.implies | u.r.lnot(a), lock=True)

        # First derivation

        section_1_2 = t.open_section(section_title='First derivation', section_number=2,
            section_parent=section_1)

        # Original: 𝑝1 ⊃ (𝑝1 ∨ 𝑝2)
        # Punctilious: 𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)
        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            line_1 = t.i.variable_substitution.infer_formula_statement(ref='1',
                p=self.pl7_statement, phi=u.r.tupl(p1, p2))

        t.take_note(
            content='"For instance, the formula on line 1, 𝑝1 ⊃ (𝑝1 ∨ 𝑝2), is an instance of axiom PL7, i.e., of 𝐴 ⊃ (𝐴 ∨ 𝐵): it is obtained by replacing 𝐴 by 𝑝1 and 𝐵 by 𝑝2. (...) In general: an instance of an instance of an axiom is an axiom", [MGZ21, p. 21]')

        # Original: [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))]
        # Punctilious: ((𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)) ⟹ (((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ⟹ (𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂))))
        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            # Original A: ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))
            a = (p1 | u.r.lor | p2) | u.r.implies | (p2 | u.r.lor | p1)
            # Original B: [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)]
            b = p1 | u.r.implies | (p1 | u.r.lor | p2)
            # Substitution tuple
            # Note that the order of variables is not alphabetical,
            # instead it must comply with the order of appearance in the formula!
            substitution_tuple: pu.Formula = u.r.tupl(b, a)
            line_2 = t.i.variable_substitution.infer_formula_statement(ref='2',
                p=self.pl5_statement, phi=substitution_tuple)

        # Original: ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))
        # Punctilious: (((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ⟹ (𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)))
        line_3 = t.i.modus_ponens.infer_formula_statement(ref='3', p_implies_q=line_2, p=line_1)

        # Original: ⊢ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] ⊃[{((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃ {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))}]
        # Punctilious: ((((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ⟹ (𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂))) ⟹ ((((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁))) ⟹ ((𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)))))
        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            # A --> ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))
            a = (p1 | u.r.lor | p2) | u.r.implies | (p2 | u.r.lor | p1)
            # B --> (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))
            b = p1 | u.r.implies | (p1 | u.r.lor | p2)
            # C --> ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))
            c = (p1 | u.r.lor | p2) | u.r.implies | (p2 | u.r.lor | p1)
            # Substitution tuple
            # Note that the order of variables is not alphabetical,
            # instead it must comply with the order of appearance in the formula!
            substitution_tuple: pu.Formula = u.r.tupl(a, b, c)
            line_4 = t.i.variable_substitution.infer_formula_statement(ref='4',
                p=self.pl3_statement, phi=substitution_tuple)

        # Original: ⊢ {((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃ {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))}
        # Punctilious: ((((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁))) ⟹ ((𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁))))
        line_5 = t.i.modus_ponens.infer_formula_statement(ref='5', p_implies_q=line_4, p=line_3)

        # Original: ⊢ [(𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))]
        # Punctilious: (((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ⟹ (((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁))))
        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            # A --> [(𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)]
            a = (p1 | u.r.lor | p2) | u.r.implies | (p2 | u.r.lor | p1)
            # Substitution tuple
            # Note that the order of variables is not alphabetical,
            # instead it must comply with the order of appearance in the formula!
            substitution_tuple: pu.Formula = u.r.tupl(a)
            line_6 = t.i.variable_substitution.infer_formula_statement(ref='6',
                p=self.pl1_statement, phi=substitution_tuple)

        # Original: ⊢ (𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)
        # Punctilious: ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁))
        # PL8: (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)
        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            # A --> 𝑝1
            # B --> 𝑝2
            a = p1
            b = p2
            # Substitution tuple
            # Note that the order of variables is not alphabetical,
            # instead it must comply with the order of appearance in the formula!
            substitution_tuple: pu.Formula = u.r.tupl(a, b)
            line_7 = t.i.variable_substitution.infer_formula_statement(ref='7',
                p=self.pl8_statement, phi=substitution_tuple)

        # Original: ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))
        # Punctilious: (((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)))
        line_8 = t.i.modus_ponens.infer_formula_statement(ref='8', p_implies_q=line_6, p=line_7)

        # Original: ⊢ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))
        # Punctilious: ((𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁)))
        line_9 = t.i.modus_ponens.infer_formula_statement(ref='9', p_implies_q=line_5, p=line_8)

        # Original: ⊢ [((𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] ⊃ (𝑝1 ⊃ (𝑝2 ∨ 𝑝1))
        # Punctilious: (((𝐩₁ ⟹ (𝐩₁ ∨ 𝐩₂)) ∧ ((𝐩₁ ∨ 𝐩₂) ⟹ (𝐩₂ ∨ 𝐩₁))) ⟹ (𝐩₁ ⟹ (𝐩₂ ∨ 𝐩₁)))
        # PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)
        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            # A --> 𝑝1
            a = p1
            # B --> (𝑝1 ∨ 𝑝2)
            b = p1 | u.r.lor | p2
            # C --> (𝑝2 ∨ 𝑝1)
            c = p2 | u.r.lor | p1
            # Substitution tuple
            # Note that the order of variables is not alphabetical,
            # instead it must comply with the order of appearance in the formula!
            substitution_tuple: pu.Formula = u.r.tupl(a, b, c)
            line_10 = t.i.variable_substitution.infer_formula_statement(ref='10',
                p=self.pl4_statement, phi=substitution_tuple)

        # Original: ⊢ 𝑝1 ⊃ (𝑝2 ∨ 𝑝1)
        # Punctilious: (𝐩₁ ⟹ (𝐩₂ ∨ 𝐩₁))
        line_11 = t.i.modus_ponens.infer_formula_statement(ref='11', p_implies_q=line_10, p=line_9)

        # Meta derivation

        section_1_3 = t.open_section(section_title='Meta derivation', section_number=3,
            section_parent=section_1)

        t.take_note(
            content='"It will be instructive to analyze the structure of the derivation. One way to understand the proof we just gave schematically is to see its first nine lines as an instance of the following (meta)derivation, where we take 𝐶 to abbreviate 𝑝 1 ⊃ (𝑝1 ∨ 𝑝2) and 𝐷 to abbreviate (𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1).", [MGZ21, p. 21]')

        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            c = u.c.declare(symbol='C', auto_index=False,
                value=p1 | u.r.implies | (p1 | u.r.lor | p2), echo=True)

        with u.with_variable(symbol='p', index=1) as p1, u.with_variable(symbol='p', index=2) as p2:
            d = u.c.declare(symbol='D', auto_index=False,
                value=(p1 | u.r.lor | p2) | u.r.implies | (p2 | u.r.lor | p1), echo=True)

        # print(t.get_first_syntactically_equivalent_statement(''
        #    formula=c))  # t.i.variable_substitution.infer_formula_statement(p=self.pl1_inclusion, phi=u.r.tupl(  #    c))  # t.i.variable_substitution.infer_formula_statement(p=line_1, phi=u.r.tupl(c, d))

        # h1: pu.Hypothesis = t.pose_hypothesis(hypothesis_formula=c)
        # h1 = t.i.variable_substitution

        # 2. ⊢ 𝐶 ⊃ (𝐷 ⊃ 𝐶)
        h1_l2 = t.i.variable_substitution.infer_formula_statement(p=self.pl5_statement,
            phi=u.r.tupl(c, d))

        # 3. ⊢ 𝐷 ⊃ 𝐶  # h1_l3 = t.i.modus_ponens.infer_formula_statement(p_implies_q=h1_l2, p=c)
        print(pu.verify_formula(u=u, input_value=c))

        phi: pu.TheoreticalObject = self.pl7_statement
        print(phi)
        psi: pu.TheoreticalObject = c.value
        print(psi)
        mask: frozenset[pu.Variable] = frozenset(
            phi.get_unique_variable_ordered_set + psi.get_unique_variable_ordered_set)
        print(mask)
        print(phi.is_alpha_equivalent_to(phi=psi))
        print(phi.is_masked_formula_similar_to(phi=psi, mask=mask))

        # print(self.pl7_statement)  # print(c.value)  # print(c.value.is_alpha_equivalent_to(phi=self.pl1_statement))

        # print(pu.verify_formula_statement(t=t, input_value=c.value))


p = MGZ2021MinimalLogicM0()
