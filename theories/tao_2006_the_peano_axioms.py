""""""
import punctilious as p

u = p.UniverseOfDiscourse()
ft = u.t(include_modus_ponens_inference_rule=True, include_conjunction_introduction_inference_rule=True,
         include_double_negation_introduction_inference_rule=True)

t = u.t(
    header=f'theory 2.1: the Peano axioms',
    extended_theory=ft, dashed_name='tao-2006-theory-2-1-the-peano-axioms')

# simple-objct declarations
zero = u.o('0')
one = u.o('1')
two = u.o('2')
three = u.o('3')
four = u.o('4')
nat = u.o('natural-number')

# relation declarations
is_a = u.r(
    2, 'is-a', p.Formula.infix_operator_representation,
    signal_proposition=True)

nla_2_1 = t.postulate_axiom(u.elaborate_axiom(f'0 is a natural number.', '2.1'))
fa_2_1_a = t.dai(u.f(is_a, zero, nat), nla_2_1, reference='2.1.a')

nla_2_2_1 = t.postulate_axiom(u.elaborate_axiom(
    'If n is a natural number, then n++ is a natural number.',
    '2.2.1'))
with u.v('n') as n:
    suc = u.r(1, '++', formula_rep=p.Formula.postfix_operator_representation, dashed_name='successor')
    fa_2_2_2 = t.dai(
        u.f(u.implies, u.f(is_a, n, nat), u.f(is_a, u.f(suc, n), nat)),
        nla_2_2_1,
        reference='2.2.2')

p_2_2_3 = t.mp(fa_2_2_2, fa_2_1_a, reference='2.2.3')
p_2_2_4 = t.mp(fa_2_2_2, p_2_2_3, reference='2.2.4')
proposition_2_2_5 = t.mp(fa_2_2_2, p_2_2_4, reference='2.2.5')

# Definition 2.1.3. We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number ((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text I use "x := y" to denote the statement that xis defined to equal y.)

definition_2_1_3 = t.d(
    'We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
    '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
    'I use "x := y" to denote the statement that x is defined to equal y.)',
    reference='2.1.3')

# 1
proposition_2_1_3_1 = t.ddi(
    u.f(u.eq, one, u.f(suc, zero)), definition_2_1_3,
    reference='2.1.3.1')

# 2
proposition_2_1_3_2 = t.ddi(
    u.f(u.eq, two, u.f(suc, u.f(suc, zero))), definition_2_1_3,
    reference='2.1.3.2')

# 3
proposition_2_1_3_3 = t.ddi(
    u.f(u.eq, three, u.f(suc, u.f(suc, u.f(suc, zero)))),
    definition_2_1_3,
    reference='2.1.3.3')

proposition_2_1_3_100 = t.mp(
    t.commutativity_of_equality, proposition_2_1_3_1, reference='2.1.3.1.b')

p_2_1_3_2_b = t.soet(
    proposition_2_1_3_2, proposition_2_1_3_100, reference='2.1.3.2.b')

p_2_1_3_2_c = t.mp(
    t.commutativity_of_equality, proposition_2_1_3_2, reference='2.1.3.2.c')

p_2_1_3_2_d = t.soet(p_2_1_3_2_c, proposition_2_1_3_100, reference='2.1.3.2.d')

p_2_1_3_3_b = t.soet(proposition_2_1_3_3, p_2_1_3_2_c, reference='2.1.3.3.b')

p_2_1_3_3_c = t.mp(
    t.commutativity_of_equality, proposition_2_1_3_3, reference='2.1.3.3.c')

p_2_1_3_3_d = t.soet(p_2_1_3_3_c, p_2_1_3_2_c, reference='2.1.3.3.d')

p_2_1_4 = t.soet(proposition_2_2_5, p_2_1_3_3_c, reference='2.1.4')

# 4
proposition_2_1_3_3 = t.ddi(
    u.f(u.eq, four, u.f(suc, u.f(suc, u.f(suc, u.f(suc, zero))))),
    definition_2_1_3,
    reference='2.1.3.3.a')

# Axiom 2.3. 0 is not the successor of any natural number;
# i.e., we have n++ f=. 0 for every natural number n.

a_2_3 = t.postulate_axiom(u.elaborate_axiom(
    '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for '
    'every natural number n.',
    '2.3'))

with u.v('n') as n:
    proposition_2_3_1 = t.dai(
        valid_proposition=u.f(
            u.implies,
            u.f(is_a, n, nat),
            u.f(ft.inequality, u.f(suc, n), zero)),
        ap=a_2_3, reference='2.3.1')


# Proposition 2.1.6. 4 is not equal to 0.
def prove_proposition_2_1_6():
    p1 = t.mp(proposition_2_3_1, proposition_2_2_5, reference='2.1.6.1')
    p2 = t.mp(
        ft.commutativity_of_equality, proposition_2_1_3_3, reference='2.1.6.2')
    p3 = t.soet(p1, p2, reference='2.1.6.3')
    pass


prove_proposition_2_1_6()
axiom_2_4 = t.postulate_axiom(u.elaborate_axiom(
    'Different natural numbers must have different successors; i.e., if n, '
    'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
    'if n++ = m++, then we must have n = m.',
    '2.4'))

with u.v('n') as n, u.v('m') as m:
    proposition_2_4_1 = t.dai(
        u.f(
            u.implies,
            u.f(
                u.conjunction_relation,
                u.f(
                    u.conjunction_relation,
                    u.f(is_a, n, nat),
                    u.f(is_a, m, nat)),
                u.f(t.inequality, n, m)),
            u.f(t.inequality, u.f(suc, n), u.f(suc, m)))
        , reference='2.4.1', ap=axiom_2_4)

# Proposition 2.1.8: 6 is not equal to 2.


# t.prnt(output_proofs=True)
