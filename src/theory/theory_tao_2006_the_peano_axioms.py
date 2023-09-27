""""""
import punctilious as pu


class Tao2006ThePeanoAxioms(pu.Package):

    def __init__(self, t: (None, pu.TheoryElaborationSequence) = None,
            u: (None, pu.UniverseOfDiscourse) = None):
        self.u = u
        self.t = t
        if self.u is None and self.t is None:
            self.u = pu.UniverseOfDiscourse()
            self.t = self.u.declare_theory()
        elif self.u is None and self.t is not None:
            self.u = self.t.u
        elif self.u is not None and self.t is None:
            self.t = self.u.declare_theory()
        u = self.u
        t = self.t

        section_2 = t.open_section('The natural numbers', section_number=2)
        section_2_1 = t.open_section('The Peano axioms', section_parent=section_2)

        # objects
        natural_number = u.o.declare(symbol='natural-number', auto_index=False)
        self.natural_number = natural_number
        zero = u.o.declare(symbol='0', auto_index=False)
        self.zero = zero
        one = u.o.declare(symbol='1', auto_index=False)
        self.one = one
        two = u.o.declare(symbol='2', auto_index=False)
        self.two = two
        three = u.o.declare(symbol='3', auto_index=False)
        self.three = three
        four = u.o.declare(symbol='4', auto_index=False)
        self.four = four
        five = u.o.declare(symbol='5', auto_index=False)
        self.five = five
        six = u.o.declare(symbol='6', auto_index=False)
        self.six = six

        # relations
        plusplus = u.r.declare(arity=1, symbol='++', auto_index=False, name='successor',
            formula_rep=pu.Formula.postfix)
        self.plusplus = plusplus

        t.open_section('Informal definition of natural number', section_parent=section_2_1,
            numbering=False)

        t.take_note(
            content='A natural number is any element of the set 𝐍 := { 0, 1, 2, 3, 4, ... }, which is the set of all the numbers created by starting with 0 and then counting forward indefinitely. We call 𝐍 the set of natural numbers.',
            paragraph_header=pu.paragraph_headers.informal_definition, ref='2.1.1')

        t.take_note(
            content='In some texts the natural numbers start at 1 instead of 0, but this is a matter of notational convention more than anything else. In this text we shall refer to the set { 1, 2, 3, ... } as the positive integers 𝐙⁺ rather than the natural numbers. Natural numbers are sometimes also known as whole numbers.',
            paragraph_header=pu.paragraph_headers.remark, ref='2.1.2')

        t.open_section('Axiom 2.1', section_parent=section_2_1, numbering=False)

        a01 = u.declare_axiom(f'0 is a natural number.')
        axiom_2_1 = t.include_axiom(a01, ref='2.1')
        self.axiom_2_1 = axiom_2_1

        # (0 is-a natural-number):
        t.i.axiom_interpretation.infer_formula_statement(axiom_2_1,
            zero | u.r.is_a | natural_number)

        t.open_section('Axiom 2.2', section_parent=section_2_1, numbering=False)

        a03 = u.declare_axiom('If n is a natural number, then n++ is a natural number.')
        axiom_2_2 = t.include_axiom(a03, ref='2.2')
        self.axiom_2_2 = axiom_2_2
        """"""

        with u.v('n') as n:
            p002 = t.i.axiom_interpretation.infer_formula_statement(axiom_2_2, (
                    (n | u.r.is_a | natural_number) | u.r.implies | (
                    (n & plusplus) | u.r.is_a | natural_number)))
        p003 = t.i.variable_substitution.infer_formula_statement(p=p002, phi=tuple([zero]))
        p004 = t.i.mp.infer_formula_statement(p003, zero | u.r.is_a | natural_number, ref='2.2.3')
        self.proposition_2_2_3 = p004

        # DEFINITION 2.1.3
        d01 = u.declare_definition(
            natural_language='We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
                             '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
                             'I use "x := y" to denote the statement that x is defined to equal y.)',
            ref='2.1.3')
        d02 = t.include_definition(d=d01)
        self.definition_2_1_3 = d02

        p005 = t.i.definition_interpretation.infer_formula_statement(d02,
            one | u.r.equal | (zero & plusplus))

        p006 = t.i.definition_interpretation.infer_formula_statement(d02,
            u.f(u.r.equal, two, ((zero & plusplus) & plusplus)))
        p007 = t.i.definition_interpretation.infer_formula_statement(d02,
            u.f(u.r.equal, three, (((zero & plusplus) & plusplus) & plusplus)))

        p008 = t.i.definition_interpretation.infer_formula_statement(d02,
            u.f(u.r.equal, four, ((((zero & plusplus) & plusplus) & plusplus) & plusplus)))

        zero_plusplus = (zero & plusplus)
        p009 = t.i.variable_substitution.infer_formula_statement(p=p002, phi=zero_plusplus)
        p010 = t.i.mp.infer_formula_statement(p009, p004)
        self.p010 = p010
        zero_plus_plus_plusplus = u.f(plusplus, zero_plusplus)
        p011 = t.i.variable_substitution.infer_formula_statement(p002, zero_plus_plus_plusplus)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₁₂): ((((0)++)++)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p012 = t.i.mp.infer_formula_statement(p011, p010)
        self.p012 = p012
        zero_plus_plus_plus_plusplus = u.f(plusplus, zero_plus_plus_plusplus)
        p013 = t.i.variable_substitution.infer_formula_statement(p002, zero_plus_plus_plus_plusplus)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₁₄): (((((0)++)++)++)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p014 = t.i.mp.infer_formula_statement(p013, p012)
        self.p014 = p014
        p015 = t.i.equality_commutativity.infer_formula_statement(p005)
        p016 = t.i.equal_terms_substitution.infer_formula_statement(p006, p015)
        p017 = t.i.equality_commutativity.infer_formula_statement(p006)
        p019 = t.i.equal_terms_substitution.infer_formula_statement(p007, p017)

        t.open_section('3 is a natural number', section_parent=section_2_1, numbering=False)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₀): ((((0)++)++)++ = 3).
        p020 = t.i.equality_commutativity.infer_formula_statement(p007)

        p021 = t.i.equal_terms_substitution.infer_formula_statement(p020, p017)
        # Proposition 2.1.4. 3 is a natural number.
        p022 = t.i.equal_terms_substitution.infer_formula_statement(p012, p020, ref='2.1.4')
        self.proposition_2_1_4 = p022

        p023 = t.i.definition_interpretation.infer_formula_statement(d02,
            u.f(u.r.equal, four, ((((zero & plusplus) & plusplus) & plusplus) & plusplus)))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₂₄): (((((0) + +) + +) + +) + + = 4).
        p024 = t.i.equality_commutativity.infer_formula_statement(p008)
        p025 = t.i.equal_terms_substitution.infer_formula_statement(p024, p020)
        p026 = t.i.equal_terms_substitution.infer_formula_statement(p013, p025)

        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₇): (4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p027 = t.i.equal_terms_substitution.infer_formula_statement(p014, p024)

        t.open_section('Axiom 2.3', section_parent=section_2_1, numbering=False)

        a05 = t.include_axiom(u.declare_axiom(
            '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for '
            'every natural number n.'), ref='2.3')

        with u.v('n') as n:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₈): ((𝐧₂ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((𝐧₂)++ ≠ 0)).
            p028 = t.i.axiom_interpretation.infer_formula_statement(a05,
                u.f(u.r.implies, (n | u.r.is_a | natural_number),
                    u.f(u.r.neq, u.f(plusplus, n), zero)))

        t.open_section('4 is not equal to 0.', section_parent=section_2_1, numbering=False)
        # Proposition 2.1.6. 4 is not equal to 0.
        t.take_note('We want to prove that 4 is not equal to 0, i.e. (4 ≠ 0).')
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: ((3 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((3)++ ≠ 0)).
        p029 = t.i.variable_substitution.infer_formula_statement(p028, three)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: ((3)++ ≠ 0).
        p030 = t.i.modus_ponens.infer_formula_statement(p029, p022)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (4 ≠ 0).
        p031 = t.i.equal_terms_substitution.infer_formula_statement(p030, p025, ref='2.1.6')

        t.open_section('Axiom 2.4', section_parent=section_2_1, numbering=False)

        axiom_2_4 = t.include_axiom(
            u.declare_axiom('Different natural numbers must have different successors; i.e., if n, '
                            'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
                            'if n++ = m++, then we must have n = m.'), ref='2.4')

        with u.v('n') as n, u.v('m') as m:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
            p032 = t.i.axiom_interpretation.infer_formula_statement(axiom_2_4, u.f(u.r.implies,
                u.f(u.r.land, u.f(u.r.land, u.f(u.r.is_a, n, natural_number),
                    u.f(u.r.is_a, m, natural_number)), u.f(u.r.neq, n, m)),
                u.f(u.r.neq, u.f(plusplus, n), u.f(plusplus, m))))
        with u.v('n') as n, u.v('m') as m:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
            p032b = t.i.axiom_interpretation.infer_formula_statement(axiom_2_4, u.f(u.r.implies,
                u.f(u.r.land, u.f(u.r.land, u.f(u.r.is_a, n, natural_number),
                    u.f(u.r.is_a, m, natural_number)),
                    u.f(u.r.equal, u.f(plusplus, n), u.f(plusplus, m))), u.f(u.r.equal, n, m)))

        s55 = t.open_section('6 is not equal to 2.', section_parent=section_2_1, numbering=False)

        # Proposition 2.1.8. 6 is not equal to 2.
        # We know that 4 is not equal to 0 from 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟮.𝟭.𝟲 (P₃₀): (4 ≠ 0).
        # With axiom 2.4 we can demonstrate that 5 is not equal to 1.
        # Take 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₁): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
        # Substitute 𝐧₃ with 4, and 𝐦₁ with 0.
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)) ⟹ ((4)++ ≠ (0)++)).
        p033 = t.i.variable_substitution.infer_formula_statement(p=p032, phi=(four, zero))
        # It follows that ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)) ⟹ ((4)++ ≠ (0)++)).
        # Pair two true propositions (4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) and (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₃₄): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p034 = t.i.conjunction_introduction.infer_formula_statement(p=p027,
            q=zero | u.r.is_a | natural_number)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₅): (((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)).
        p035 = t.i.conjunction_introduction.infer_formula_statement(p=p034, q=p031)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₆): ((4)++ ≠ (0)++).
        p036 = t.i.modus_ponens.infer_formula_statement(p033, p035)

        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₇): (5 = (((((0)++)++)++)++)++).
        p037 = t.i.definition_interpretation.infer_formula_statement(d02, u.f(u.r.equal, five,
            u.f(plusplus, ((((zero & plusplus) & plusplus) & plusplus) & plusplus))))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₈): ((((((0)++)++)++)++)++ = 5).
        p038 = t.i.equality_commutativity.infer_formula_statement(p037)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₉): ((4)++ = 5).
        p039 = t.i.equal_terms_substitution.infer_formula_statement(p038, p024)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₀): (5 = (4)++).
        p040 = t.i.equality_commutativity.infer_formula_statement(p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₁): ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)) ⟹ ((5)++ ≠ (1)++)).
        p041 = t.i.variable_substitution.infer_formula_statement(p=p032, phi=(five, one))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₂): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((4)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p042 = t.i.variable_substitution.infer_formula_statement(p002, four)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₃): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ (5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p043 = t.i.equal_terms_substitution.infer_formula_statement(p042, p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₄₄): (5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p044 = t.i.modus_ponens.infer_formula_statement(p043, p027)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₅): ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)) ⟹ ((5)++ ≠ (1)++)).
        p045 = t.i.variable_substitution.infer_formula_statement(p=p032, phi=(five, one))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₆): ((4)++ ≠ (0)++).
        p046 = t.i.modus_ponens.infer_formula_statement(p033, p035)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₇): (5 ≠ (0)++).
        p047 = t.i.equal_terms_substitution.infer_formula_statement(p=p046, x_equal_y=p039)

        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (6 = ((((((0)++)++)++)++)++)++).
        p049 = t.i.definition_interpretation.infer_formula_statement(d02, u.f(u.r.equal, six,
            u.f(plusplus, u.f(plusplus, ((((zero & plusplus) & plusplus) & plusplus) & plusplus)))))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (((((((0)++)++)++)++)++)++ = 6).
        p050 = t.i.equality_commutativity.infer_formula_statement(p049)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₄): (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p054 = t.i.equal_terms_substitution.infer_formula_statement(p004, p015)
        p051 = t.i.equal_terms_substitution.infer_formula_statement(p050, p038)
        # (6 = (5)++)
        p057 = t.i.equality_commutativity.infer_formula_statement(x_equal_y=p051)

        t.open_section('Proof by contradiction', section_parent=s55, numbering=False)

        t.take_note(
            content='First, we follow (Tao 2006)''s proof by contradiction. In punctilious, we use the term proof-by-refutation-of-equality to designate this specific method of proof.')

        # Proof.
        # Suppose for sake of contradiction that 6 = 2.
        h1 = t.pose_hypothesis(hypothesis_formula=six | u.r.eq | two)
        hypothesis_statement = h1.hypothesis_statement_in_child_theory
        # Then 5++ = 1++,
        # ((5)++ = 2)
        h1_p2 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_formula_statement(
            p=hypothesis_statement, x_equal_y=p057)
        # ((5)++ = (1)++)
        h1_p3 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_formula_statement(
            p=h1_p2, x_equal_y=p016)
        # so by Axiom 2.4 we have 5 = 1
        # ((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟))
        h1_p4 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_formula_statement(
            p=p044, q=p054)
        # (((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((5)++ = (1)++))
        h1_p5 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_formula_statement(
            p=h1_p4, q=h1_p3)
        # ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((5)++ = (1)++)) ⟹ (5 = 1))
        h1_p6 = h1.hypothesis_child_theory.i.variable_substitution.infer_formula_statement(p=p032b,
            phi=tuple([five, one]))
        # (5 = 1)
        h1_p7 = h1.hypothesis_child_theory.i.modus_ponens.infer_formula_statement(p_implies_q=h1_p6,
            p=h1_p5)
        # so that 4++ = 0++.
        # ((4)++ = 1)
        h1_p8 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_formula_statement(
            p=h1_p7, x_equal_y=p040)
        # ((4)++ = (0)++)
        h1_p9 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_formula_statement(
            p=h1_p8, x_equal_y=p005)

        # ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟))
        h1_p10 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_formula_statement(
            p=p027, q=zero | u.r.is_a | natural_number)
        # (((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((4)++ = (0)++))
        h1_p11 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_formula_statement(
            p=h1_p10, q=h1_p9)
        # ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((4)++ = (0)++)) ⟹ (4 = 0))
        h1_p12 = h1.hypothesis_child_theory.i.variable_substitution.infer_formula_statement(p=p032b,
            phi=tuple([four, zero]))
        # (4 = 0)
        # By Axiom 2.4 again we then have 4 = 0, which contradicts our previous proposition.
        h1_p071 = h1.hypothesis_child_theory.i.modus_ponens.infer_formula_statement(
            p_implies_q=h1_p12, p=h1_p11)
        p072 = t.i.inconsistency_introduction_2.infer_formula_statement(x_eq_y=h1_p071,
            x_neq_y=p031, inconsistent_theory=h1.hypothesis_child_theory)
        p073 = t.i.proof_by_refutation_2.infer_formula_statement(x_eq_y_hypothesis=h1,
            inc_hypothesis=p072, ref='2.1.8')

        t.open_section('Direct proof', section_parent=s55, numbering=False)

        t.take_note(
            content='In (Tao, 2006), proposition 2.1.8 uses proof by contradiction. Note that in punctilious, this specific proof method is called a proof by refutation of equality. Nevertheless, proofs by contradictions are somehow indirect proofs. As an alternative, we now propose a direct proof.')
        p018 = t.i.equal_terms_substitution.infer_formula_statement(p017, p015)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (5 ≠ 1).
        p048 = t.i.equal_terms_substitution.infer_formula_statement(p047, p015)
        # ((5)++ = 6).
        p052 = t.i.equal_terms_substitution.infer_formula_statement(p045, p051)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)).
        p053 = t.i.equal_terms_substitution.infer_formula_statement(p052, p018)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: ((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p055 = t.i.conjunction_introduction.infer_formula_statement(p044, p054)
        p056 = t.i.conjunction_introduction.infer_formula_statement(p055, p048)
        p057 = t.i.modus_ponens.infer_formula_statement(p_implies_q=p053, p=p056)

        t.open_section('Axiom 2.5: The principle of mathematical induction',
            section_parent=section_2_1, numbering=False)

        a_2_5 = u.declare_axiom(paragraph_header=pu.paragraph_headers.axiom_schema_declaration,
            subtitle='Principle of mathematical induction',
            natural_language='Let P(n) be any property pertaining to a natural number n. Suppose that P(O) is true, and suppose that whenever P(n) is true, P(n++) is also true. Then P(n) is true for every natural number n.')

        a_2_5b = t.include_axiom(a=a_2_5,
            paragraph_header=pu.paragraph_headers.axiom_schema_inclusion,
            subtitle='Principle of mathematical induction')

        with u.v('P') as p, u.v('n') as n, u.v('m') as m:
            # P is-a unary-relation
            # phi1 = (p | u.r.is_a | u.o.relation)
            # n is-a natural-number
            phi2 = (n | u.r.is_a | natural_number)
            # P(0)
            phi3 = p(zero)  # TODO: Implement this syntax
            # P(n) ⟹ P(n++)
            phi4 = (p(n) | u.r.implies | p(n & plusplus))
            phi5 = (phi2 | u.r.land | (phi3 | u.r.land | phi4))
            # ⟹
            # ((m is-a natural-number) ⟹ P(m))
            phi6 = (m | u.r.is_a | natural_number) | u.r.implies | p(m)
            phi7 = phi5 | u.r.implies | phi6
            p100 = t.i.axiom_interpretation.infer_formula_statement(a=a_2_5b, formula=phi7)

        t.take_note(paragraph_header=pu.paragraph_headers.remark, ref='2.1.10',
            content='We are a little vague on what "property" means at this point, but some possible examples of P(n) might be "n is even"; "n is equal to 3"; "n solves the equation (n + 1)2 = n2 + 2n + 1"; and so forth. Of course we haven\'t defined many of these concepts yet, but when we do, Axiom 2.5 will apply to these properties. (A logical remark: Because this axiom refers not just to variables, but also properties, it is of a different nature than the other four axioms; indeed, Axiom 2.5 should technically be called an axiom schema rather than an axiom - it is a template for producing an (infinite) number of axioms, rather than being a single axiom in its own right. To discuss this distinction further is far beyond the scope of this text, though, and falls in the realm of logic.) [Tao, 2006, p. 22]')

        # TODO: Include sample proposition 2.1.11 (Tao 2006, p. 23) in an hypothesis.

        t.open_section('The number system N', section_parent=section_2_1, numbering=False)

        t.take_note(paragraph_header=pu.paragraph_headers.informal_assumption, ref='2.6',
            content='There exists a number system N, whose elements we will call natural numbers, for which Axioms 2.1-2.5 are true.')

        t.open_section('Recursive definitions', section_parent=section_2_1, numbering=False)

        t.take_note(paragraph_header=pu.paragraph_headers.informal_proposition, ref='2.1.16',
            subtitle='recursive definitions',
            content='Suppose for each natural number n, we have some function fₙ : N -> N from the natural numbers to the natural numbers. Let c be a natural number. Then we can assign a unique natural number an to each natural number n, such that a₀ = c and aₙ₊₊ = fₙ(aₙ) for each natural number n.')

        t.take_note(paragraph_header=pu.paragraph_headers.informal_proof,
            content='We use induction. We first observe that this procedure gives a single value to a₀, namely c. (None of the other definitions aₙ₊₊ := fₙ(aₙ) will redefine the value of a₀, because of Axiom 2.3.) Now suppose inductively that the procedure gives a single value to aₙ. Then it gives a single value to aₙ₊₊, namely aₙ₊₊ := fₙ(aₙ). (None of the other definitions aₘ₊₊ := fₘ(aₘ) will redefine the value of aₙ₊₊, because of Axiom 2.4.) This completes the induction, and so aₙ is defined for each natural number n, with a single value assigned to each aₙ.')

        # TODO: Provide a formal proof of recursive definitions.
