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
            cat=pu.title_categories.informal_definition,
            ref='2.1.1')

        t.take_note(
            content='In some texts the natural numbers start at 1 instead of 0, but this is a matter of notational convention more than anything else. In this text we shall refer to the set { 1, 2, 3, ... } as the positive integers 𝐙⁺ rather than the natural numbers. Natural numbers are sometimes also known as whole numbers.',
            cat=pu.title_categories.remark,
            ref='2.1.2')

        # AXIOM 2.1.1
        a01 = u.declare_axiom(f'0 is a natural number.')
        a02 = t.include_axiom(a01, ref='2.1')
        zero = u.o.declare(symbol='0', auto_index=False)
        natural_number = u.o.declare(symbol='natural-number', auto_index=False)
        is_a = u.r.declare(arity=2, symbol='is-a', auto_index=False, formula_rep=pu.Formula.infix,
                           signal_proposition=True)
        # (0 is-a natural-number):
        p001 = t.i.axiom_interpretation.infer_statement(a02, u.f(is_a, zero, natural_number))

        # AXIOM 2.1.2

        a03 = u.declare_axiom('If n is a natural number, then n++ is a natural number.')
        a04 = t.include_axiom(a03, ref='2.2')
        plusplus = u.r.declare(arity=1, symbol='++', auto_index=False, name='successor',
                               formula_rep=pu.Formula.postfix)
        with u.v('n') as n:
            p002 = t.i.axiom_interpretation.infer_statement(
                a04,
                u.f(u.r.implies, u.f(is_a, n, natural_number),
                    u.f(is_a, u.f(plusplus, n), natural_number)))
        p003 = t.i.variable_substitution.infer_statement(p002, zero)
        p004 = t.i.mp.infer_statement(p003, p001, ref='2.2.3')

        # DEFINITION 2.1.3

        d01 = u.declare_definition(
            natural_language='We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
                             '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
                             'I use "x := y" to denote the statement that x is defined to equal y.)',
            ref='2.1.3')
        d02 = t.include_definition(d=d01)
        one = u.o.declare(symbol='1', auto_index=False)
        p005 = t.i.definition_interpretation.infer_statement(
            d02, u.f(u.r.equal, one, u.f(plusplus, zero)))
        two = u.o.declare(symbol='2', auto_index=False)
        p006 = t.i.definition_interpretation.infer_statement(
            d02, u.f(u.r.equal, two, u.f(plusplus, u.f(plusplus, zero))))
        three = u.o.declare(symbol='3', auto_index=False)
        p007 = t.i.definition_interpretation.infer_statement(
            d02, u.f(u.r.equal, three, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero)))))
        four = u.o.declare(symbol='4', auto_index=False)
        p008 = t.i.definition_interpretation.infer_statement(
            d02,
            u.f(u.r.equal, four, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero))))))

        zero_plusplus = u.f(plusplus, zero)
        p009 = t.i.variable_substitution.infer_statement(p002, zero_plusplus)
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
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₀): ((((0)++)++)++ = 3).
        p020 = t.i.equality_commutativity.infer_statement(p007)
        p021 = t.i.equal_terms_substitution.infer_statement(p020, p017)

        # Proposition 2.1.4. 3 is a natural number.
        p022 = t.i.equal_terms_substitution.infer_statement(p012, p020, ref='2.1.4')

        p023 = t.i.definition_interpretation.infer_statement(
            d02,
            u.f(u.r.equal, four, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero))))))
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
            p028 = t.i.axiom_interpretation.infer_statement(
                a05, u.f(u.r.implies, u.f(is_a, n, natural_number),
                         u.f(u.r.neq, u.f(plusplus, n), zero)))

        # Proposition 2.1.6. 4 is not equal to 0.
        t.take_note('We want to prove that 4 is not equal to 0, i.e. (4 ≠ 0).')
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₂₉): ((3 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((3)++ ≠ 0)).
        p029 = t.i.variable_substitution.infer_statement(p028, three)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₃₀): ((3)++ ≠ 0).
        p030 = t.i.modus_ponens.infer_statement(p029, p022)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟮.𝟭.𝟲 (P₃₁): (4 ≠ 0).
        p031 = t.i.equal_terms_substitution.infer_statement(p030, p025, ref='2.1.6')

        axiom_2_4 = t.include_axiom(u.declare_axiom(
            'Different natural numbers must have different successors; i.e., if n, '
            'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
            'if n++ = m++, then we must have n = m.'), ref='2.4')

        with u.v('n') as n, u.v('m') as m:
            # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
            p032 = t.i.axiom_interpretation.infer_statement(
                axiom_2_4,
                u.f(
                    u.r.implies,
                    u.f(
                        u.r.land,
                        u.f(
                            u.r.land,
                            u.f(is_a, n, natural_number),
                            u.f(is_a, m, natural_number)),
                        u.f(u.r.neq, n, m)),
                    u.f(u.r.neq, u.f(plusplus, n), u.f(plusplus, m))))

        # Proposition 2.1.8. 6 is not equal to 2.
        # We know that 4 is not equal to 0 from 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟮.𝟭.𝟲 (P₃₀): (4 ≠ 0).
        # With axiom 2.4 we can demonstrate that 5 is not equal to 1.
        # Take 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₁): ((((𝐧₃ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (𝐦₁ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (𝐧₃ ≠ 𝐦₁)) ⟹ ((𝐧₃)++ ≠ (𝐦₁)++)).
        # Substitute 𝐧₃ with 4, and 𝐦₁ with 0.
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₂): ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)) ⟹ ((4)++ ≠ (0)++)).
        p033 = t.i.variable_substitution.infer_statement(p032, four, zero)
        # It follows that ((((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)) ⟹ ((4)++ ≠ (0)++)).
        # Pair two true propositions (4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) and (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₃₄): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p034 = t.i.conjunction_introduction.infer_statement(p027, p001)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₅): (((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (0 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (4 ≠ 0)).
        p035 = t.i.conjunction_introduction.infer_statement(p034, p031)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₆): ((4)++ ≠ (0)++).
        p036 = t.i.modus_ponens.infer_statement(p033, p035)
        five = u.o.declare(symbol='5', auto_index=False)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₇): (5 = (((((0)++)++)++)++)++).
        p037 = t.i.definition_interpretation.infer_statement(
            d02,
            u.f(u.r.equal, five,
                u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero)))))))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₈): ((((((0)++)++)++)++)++ = 5).
        p038 = t.i.equality_commutativity.infer_statement(p037)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₃₉): ((4)++ = 5).
        p039 = t.i.equal_terms_substitution.infer_statement(p038, p024)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₀): (5 = (4)++).
        p040 = t.i.equality_commutativity.infer_statement(p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₁): ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)) ⟹ ((5)++ ≠ (1)++)).
        p041 = t.i.variable_substitution.infer_statement(p032, five, one)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₂): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ ((4)++ 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p042 = t.i.variable_substitution.infer_statement(p002, four)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₃): ((4 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ⟹ (5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p043 = t.i.equal_terms_substitution.infer_statement(p042, p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻(P₄₄): (5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p044 = t.i.modus_ponens.infer_statement(p043, p027)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₅): ((((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)) ⟹ ((5)++ ≠ (1)++)).
        p045 = t.i.variable_substitution.infer_statement(p032, five, one)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₆): ((4)++ ≠ (0)++).
        p046 = t.i.modus_ponens.infer_statement(p033, p035)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₇): (5 ≠ (0)++).
        p047 = t.i.equal_terms_substitution.infer_statement(p046, p039)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₄₈): (5 ≠ 1).
        p048 = t.i.equal_terms_substitution.infer_statement(p047, p015)
        six = u.o.declare(symbol='6', auto_index=False)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (6 = ((((((0)++)++)++)++)++)++).
        p049 = t.i.definition_interpretation.infer_statement(
            d02,
            u.f(u.r.equal, six,
                u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus,
                                                                                          zero))))))))
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻: (((((((0)++)++)++)++)++)++ = 6).
        p050 = t.i.equality_commutativity.infer_statement(p049)
        p051 = t.i.equal_terms_substitution.infer_statement(p050, p038)
        p052 = t.i.equal_terms_substitution.infer_statement(p045, p051)
        p053 = t.i.equal_terms_substitution.infer_statement(p052, p018)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₄): (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟).
        p054 = t.i.equal_terms_substitution.infer_statement(p004, p015)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₅): ((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)).
        p055 = t.i.conjunction_introduction.infer_statement(p044, p054)
        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 (P₅₆): (((5 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟) ∧ (1 𝑖𝑠-𝑎 𝑛𝑎𝑡𝑢𝑟𝑎𝑙-𝑛𝑢𝑚𝑏𝑒𝑟)) ∧ (5 ≠ 1)).
        p056 = t.i.conjunction_introduction.infer_statement(p055, p048)

        # 𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 2.1.8: (6 ≠ 2).
        # Direct proof:
        p057 = t.i.modus_ponens.infer_statement(p053, p056, ref='2.1.8')
        t.take_note(
            content='Proposition 2.1.8 was demonstrated by direct proof. But (Tap 2006) proposes a proof by contradiction which seem simpler. So let us provide a second proof, by contradiction this time.')

        # Proof by contradiction:
        # TODO: Implement proof by contradiction.

# test = Tao2006ThePeanoAxioms()
# test.develop()