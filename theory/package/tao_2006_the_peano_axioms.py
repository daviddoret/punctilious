""""""
import punctilious as pu


# pu.configuration.echo_default = True
# pu.configuration.echo_axiom_declaration = True
# pu.configuration.echo_axiom_inclusion = True
# pu.configuration.echo_definition_declaration = True
# pu.configuration.echo_definition_inclusion = True
# pu.configuration.echo_inferred_statement = True
# pu.configuration.echo_proof = False
# pu.configuration.echo_simple_objct_declaration = True
# pu.configuration.echo_statement = True
# pu.configuration.echo_relation = True


class Tao2006ThePeanoAxioms(pu.TheoryPackage):
    def develop_theory(self, t: pu.TheoryElaborationSequence) -> pu.TheoryElaborationSequence:
        u = t.u
        section_2 = t.open_section('The natural numbers', section_number=2)
        section_2_1 = t.open_section('The Peano axioms', section_parent=section_2)

        t.take_note(
            content='A natural number is any element of the set 𝐍 := { 0, 1, 2, 3, 4, ... }, which is the set of all the numbers created by starting with 0 and then counting forward indefinitely. We call 𝐍 the set of natural numbers.',
            paragraph_header=pu.paragraph_headers.informal_definition, ref='2.1.1')

        t.take_note(
            content='In some texts the natural numbers start at 1 instead of 0, but this is a matter of notational convention more than anything else. In this text we shall refer to the set { 1, 2, 3, ... } as the positive integers 𝐙⁺ rather than the natural numbers. Natural numbers are sometimes also known as whole numbers.',
            paragraph_header=pu.paragraph_headers.remark, ref='2.1.2')

        # AXIOM 2.1.1
        a01 = u.declare_axiom(f'0 is a natural number.')
        a02 = t.include_axiom(a01, ref='2.1')
        zero = u.o.declare(symbol='0', auto_index=False)
        natural_number = u.o.declare(symbol='natural-number', auto_index=False)
        is_a = u.r.declare(arity=2, symbol='is-a', auto_index=False, formula_rep=pu.Formula.infix,
            signal_proposition=True)
        # (0 is-a natural-number):
        p001 = t.i.axiom_interpretation.infer_statement(a02, zero | is_a | natural_number)

        # AXIOM 2.1.2

        a03 = u.declare_axiom('If n is a natural number, then n++ is a natural number.')
        a04 = t.include_axiom(a03, ref='2.2')
        plusplus = u.r.declare(arity=1, symbol='++', auto_index=False, name='successor',
            formula_rep=pu.Formula.postfix)
        with u.v('n') as n:
            p002 = t.i.axiom_interpretation.infer_statement(a04, (
                    (n | is_a | natural_number) | u.r.implies | (
                    (n & plusplus) | is_a | natural_number)))
        p003 = t.i.variable_substitution.infer_statement(p=p002, phi=tuple([zero]))
        p004 = t.i.mp.infer_statement(p003, p001, ref='2.2.3')

        # DEFINITION 2.1.3

        d01 = u.declare_definition(
            natural_language='We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
                             '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
                             'I use "x := y" to denote the statement that x is defined to equal y.)',
            ref='2.1.3')
        d02 = t.include_definition(d=d01)
        one = u.o.declare(symbol='1', auto_index=False)
        p005 = t.i.definition_interpretation.infer_statement(d02,
            u.f(u.r.equal, one, (zero & plusplus)))
        two = u.o.declare(symbol='2', auto_index=False)
        p006 = t.i.definition_interpretation.infer_statement(d02,
            u.f(u.r.equal, two, ((zero & plusplus) & plusplus)))
        three = u.o.declare(symbol='3', auto_index=False)
        p007 = t.i.definition_interpretation.infer_statement(d02,
            u.f(u.r.equal, three, (((zero & plusplus) & plusplus) & plusplus)))
        four = u.o.declare(symbol='4', auto_index=False)
        p008 = t.i.definition_interpretation.infer_statement(d02,
            u.f(u.r.equal, four, ((((zero & plusplus) & plusplus) & plusplus) & plusplus)))

        zero_plusplus = (zero & plusplus)
        p009 = t.i.variable_substitution.infer_statement(p=p002, phi=zero_plusplus)
        p010 = t.i.mp.infer_statement(p009, p004)
        zero_plus_plus_plusplus = u.f(plusplus, zero_plusplus)
        p011 = t.i.variable_substitution.infer_statement(p002, zero_plus_plus_plusplus)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₁₂): ((((0)++)++)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p012 = t.i.mp.infer_statement(p011, p010)
        zero_plus_plus_plus_plusplus = u.f(plusplus, zero_plus_plus_plusplus)
        p013 = t.i.variable_substitution.infer_statement(p002, zero_plus_plus_plus_plusplus)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₁₄): (((((0)++)++)++)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p014 = t.i.mp.infer_statement(p013, p012)
        p015 = t.i.equality_commutativity.infer_statement(p005)
        p016 = t.i.equal_terms_substitution.infer_statement(p006, p015)
        p017 = t.i.equality_commutativity.infer_statement(p006)
        p018 = t.i.equal_terms_substitution.infer_statement(p017, p015)
        p019 = t.i.equal_terms_substitution.infer_statement(p007, p017)

        t.open_section('3 is a natural number', section_parent=section_2_1, section_number=3)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₀): ((((0)++)++)++ = 3).
        p020 = t.i.equality_commutativity.infer_statement(p007)
        # Proposition 2.1.4. 3 is a natural number.
        p022 = t.i.equal_terms_substitution.infer_statement(p012, p020, ref='2.1.4')

        p021 = t.i.equal_terms_substitution.infer_statement(p020, p017)

        p023 = t.i.definition_interpretation.infer_statement(d02,
            u.f(u.r.equal, four, ((((zero & plusplus) & plusplus) & plusplus) & plusplus)))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₂₄): (((((0) + +) + +) + +) + + = 4).
        p024 = t.i.equality_commutativity.infer_statement(p008)
        p025 = t.i.equal_terms_substitution.infer_statement(p024, p020)
        p026 = t.i.equal_terms_substitution.infer_statement(p013, p025)

        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₇): (4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p027 = t.i.equal_terms_substitution.infer_statement(p014, p024)

        a05 = t.include_axiom(u.declare_axiom(
            '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for '
            'every natural number n.'), ref='2.3')

        with u.v('n') as n:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₈): ((𝐧₂ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((𝐧₂)++ ≠ 0)).
            p028 = t.i.axiom_interpretation.infer_statement(a05,
                u.f(u.r.implies, u.f(is_a, n, natural_number),
                    u.f(u.r.neq, u.f(plusplus, n), zero)))

        # Proposition 2.1.6. 4 is not equal to 0.
        t.take_note('We want to prove that 4 is not equal to 0, i.e. (4 ≠ 0).')
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₉): ((3 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((3)++ ≠ 0)).
        p029 = t.i.variable_substitution.infer_statement(p028, three)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₃₀): ((3)++ ≠ 0).
        p030 = t.i.modus_ponens.infer_statement(p029, p022)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟮.𝟭.𝟲 (P₃₁): (4 ≠ 0).
        p031 = t.i.equal_terms_substitution.infer_statement(p030, p025, ref='2.1.6')

        axiom_2_4 = t.include_axiom(
            u.declare_axiom('Different natural numbers must have different successors; i.e., if n, '
                            'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
                            'if n++ = m++, then we must have n = m.'), ref='2.4')

        with u.v('n') as n, u.v('m') as m:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
            p032 = t.i.axiom_interpretation.infer_statement(axiom_2_4, u.f(u.r.implies,
                u.f(u.r.land,
                    u.f(u.r.land, u.f(is_a, n, natural_number), u.f(is_a, m, natural_number)),
                    u.f(u.r.neq, n, m)), u.f(u.r.neq, u.f(plusplus, n), u.f(plusplus, m))))
        with u.v('n') as n, u.v('m') as m:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
            p032b = t.i.axiom_interpretation.infer_statement(axiom_2_4, u.f(u.r.implies,
                u.f(u.r.land,
                    u.f(u.r.land, u.f(is_a, n, natural_number), u.f(is_a, m, natural_number)),
                    u.f(u.r.equal, u.f(plusplus, n), u.f(plusplus, m))), u.f(u.r.equal, n, m)))
        # Proposition 2.1.8. 6 is not equal to 2.
        # We know that 4 is not equal to 0 from 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟮.𝟭.𝟲 (P₃₀): (4 ≠ 0).
        # With axiom 2.4 we can demonstrate that 5 is not equal to 1.
        # Take 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₁): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
        # Substitute 𝐧₃ with 4, and 𝐦₁ with 0.
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)) ⟹ ((4)++ ≠ (0)++)).
        p033 = t.i.variable_substitution.infer_statement(p=p032, phi=(four, zero))
        # It follows that ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)) ⟹ ((4)++ ≠ (0)++)).
        # Pair two true propositions (4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) and (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₃₄): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p034 = t.i.conjunction_introduction.infer_statement(p=p027, q=p001)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₅): (((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)).
        p035 = t.i.conjunction_introduction.infer_statement(p=p034, q=p031)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₆): ((4)++ ≠ (0)++).
        p036 = t.i.modus_ponens.infer_statement(p033, p035)
        five = u.o.declare(symbol='5', auto_index=False)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₇): (5 = (((((0)++)++)++)++)++).
        p037 = t.i.definition_interpretation.infer_statement(d02, u.f(u.r.equal, five,
            u.f(plusplus, ((((zero & plusplus) & plusplus) & plusplus) & plusplus))))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₈): ((((((0)++)++)++)++)++ = 5).
        p038 = t.i.equality_commutativity.infer_statement(p037)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₉): ((4)++ = 5).
        p039 = t.i.equal_terms_substitution.infer_statement(p038, p024)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₀): (5 = (4)++).
        p040 = t.i.equality_commutativity.infer_statement(p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₁): ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)) ⟹ ((5)++ ≠ (1)++)).
        p041 = t.i.variable_substitution.infer_statement(p=p032, phi=(five, one))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₂): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((4)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p042 = t.i.variable_substitution.infer_statement(p002, four)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₃): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ (5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p043 = t.i.equal_terms_substitution.infer_statement(p042, p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₄₄): (5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p044 = t.i.modus_ponens.infer_statement(p043, p027)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₅): ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)) ⟹ ((5)++ ≠ (1)++)).
        p045 = t.i.variable_substitution.infer_statement(p=p032, phi=(five, one))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₆): ((4)++ ≠ (0)++).
        p046 = t.i.modus_ponens.infer_statement(p033, p035)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₇): (5 ≠ (0)++).
        p047 = t.i.equal_terms_substitution.infer_statement(p=p046, q_equal_r=p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₈): (5 ≠ 1).
        p048 = t.i.equal_terms_substitution.infer_statement(p047, p015)
        six = u.o.declare(symbol='6', auto_index=False)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (6 = ((((((0)++)++)++)++)++)++).
        p049 = t.i.definition_interpretation.infer_statement(d02, u.f(u.r.equal, six,
            u.f(plusplus, u.f(plusplus, ((((zero & plusplus) & plusplus) & plusplus) & plusplus)))))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (((((((0)++)++)++)++)++)++ = 6).
        p050 = t.i.equality_commutativity.infer_statement(p049)
        # ((5)++ = 6).
        p051 = t.i.equal_terms_substitution.infer_statement(p050, p038)
        p052 = t.i.equal_terms_substitution.infer_statement(p045, p051)
        p053 = t.i.equal_terms_substitution.infer_statement(p052, p018)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₄): (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p054 = t.i.equal_terms_substitution.infer_statement(p004, p015)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₅): ((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p055 = t.i.conjunction_introduction.infer_statement(p044, p054)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₆): (((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)).
        p056 = t.i.conjunction_introduction.infer_statement(p055, p048)
        # (6 = (5)++)
        p057 = t.i.equality_commutativity.infer_statement(p_eq_q=p051)

        section_2_1_8 = t.open_section('6 is not equal to 2', section_parent=section_2_1,
            section_number=8)

        t.take_note(content='First, we follow (Tao 2006)''s proof by contradiction.')

        # Proof.
        # Suppose for sake of contradiction that 6 = 2.
        h1 = t.pose_hypothesis(hypothesis_formula=u.f(u.r.equality, six, two))
        hypothesis_statement = h1.hypothesis_statement_in_child_theory
        # Then 5++ = 1++,
        # ((5)++ = 2)
        h1_p2 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_statement(
            p=hypothesis_statement, q_equal_r=p057)
        # ((5)++ = (1)++)
        h1_p3 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_statement(p=h1_p2,
            q_equal_r=p016)
        # so by Axiom 2.4 we have 5 = 1
        # ((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟))
        h1_p4 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_statement(p=p044,
            q=p054)
        # (((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((5)++ = (1)++))
        h1_p5 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_statement(p=h1_p4,
            q=h1_p3)
        # ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((5)++ = (1)++)) ⟹ (5 = 1))
        h1_p6 = h1.hypothesis_child_theory.i.variable_substitution.infer_statement(p=p032b,
            phi=tuple([five, one]))
        # (5 = 1)
        h1_p7 = h1.hypothesis_child_theory.i.modus_ponens.infer_statement(p_implies_q=h1_p6,
            p=h1_p5)
        # so that 4++ = 0++.
        # ((4)++ = 1)
        h1_p8 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_statement(p=h1_p7,
            q_equal_r=p040)
        # ((4)++ = (0)++)
        h1_p9 = h1.hypothesis_child_theory.i.equal_terms_substitution.infer_statement(p=h1_p8,
            q_equal_r=p005)

        # ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟))
        h1_p10 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_statement(p=p027,
            q=p001)
        # (((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((4)++ = (0)++))
        h1_p11 = h1.hypothesis_child_theory.i.conjunction_introduction.infer_statement(p=h1_p10,
            q=h1_p9)
        # ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ ((4)++ = (0)++)) ⟹ (4 = 0))
        h1_p12 = h1.hypothesis_child_theory.i.variable_substitution.infer_statement(p=p032b,
            phi=tuple([four, zero]))
        # (4 = 0)
        # By Axiom 2.4 again we then have 4 = 0, which contradicts our previous proposition.
        h1_p071 = h1.hypothesis_child_theory.i.modus_ponens.infer_statement(p_implies_q=h1_p12,
            p=h1_p11)
        p072 = t.i.inconsistency_by_inequality_introduction.infer_statement(p_eq_q=h1_p071,
            p_neq_q=p031, inconsistent_theory=h1.hypothesis_child_theory)
        p073 = t.i.proof_by_refutation_of_equality.infer_statement(p_eq_q=h1, inc_p_eq_q=p072,
            ref='2.1.8')
        pass
        t.take_note(
            content='In (Tao, 2006), proposition 2.1.8 uses proof by contradiction. Note that in punctilious, this specific proof method is called a proof by refutation of equality. Nevertheless, proofs by contradictions are somehow indirect proofs. As an alternative, we now propose a direct proof.')
        # TODO: Tao 2006: Bring back direct proof dependent propositions here
        p057 = t.i.modus_ponens.infer_statement(p_implies_q=p053, p=p056)

        # Proof by contradiction:  # TODO: Implement proof by contradiction.
        pass
