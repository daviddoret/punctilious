from punctilious import Formula, ft, u

t = u.t(
    symbol=f'theory 2.1: the Peano axioms',
    extended_theories={ft}, theory_foundation_system=ft)

# simple-objct declarations
zero = u.o('0')
one = u.o('1')
two = u.o('2')
three = u.o('3')
nat = u.o('natural-number')

# relation declarations
is_a = u.r(
    2, 'is-a', Formula.infix_operator_representation,
    signal_proposition=True)

nla_2_1 = t.nla(f'0 is a natural number.', reference='2.1')
fa_2_1_a = t.fa(u.f(is_a, zero, nat), nla_2_1, reference='2.1.a')

nla_2_2_1 = t.nla(
    'If n is a natural number, then n++ is a natural number.',
    reference='2.2.1')
with u.v('n') as n:
    suc = u.r(1, '++', formula_rep=Formula.postfix_operator_representation)
    fa_2_2_2 = t.fa(
        u.f(ft.implication, u.f(is_a, n, nat), u.f(is_a, u.f(suc, n), nat)),
        nla_2_2_1,
        reference='2.2.2')

p_2_2_3 = t.mp(fa_2_2_2, fa_2_1_a, reference='2.2.3')
p_2_2_4 = t.mp(fa_2_2_2, p_2_2_3, reference='2.2.4')
p_2_2_5 = t.mp(fa_2_2_2, p_2_2_4, reference='2.2.5')

d_2_1_3 = t.nld(
    'We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
    '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
    'I use "x := y" to denote the statement that x is defined to equal y.)',
    reference='2.1.3')

# 1
fd_2_1_3_1_a = t.fd(
    u.f(t.equality, one, u.f(suc, zero)), d_2_1_3, reference='2.1.3.1.a')

p_2_1_3_1_b = t.mp(
    t.commutativity_of_equality, fd_2_1_3_1_a, reference='2.1.3.1.b')

# 2
fd_2_1_3_2_a = t.fd(
    u.f(t.equality, two, u.f(suc, u.f(suc, zero))), d_2_1_3,
    reference='2.1.3.2.a')
p_2_1_3_2_b = t.soet(fd_2_1_3_2_a, p_2_1_3_1_b, reference='2.1.3.2.b')

p_2_1_3_2_c = t.mp(
    t.commutativity_of_equality, fd_2_1_3_2_a, reference='2.1.3.2.c')

p_2_1_3_2_d = t.soet(p_2_1_3_2_c, p_2_1_3_1_b, reference='2.1.3.2.d')

# 3
fd_2_1_3_3_a = t.fd(
    u.f(t.equality, three, u.f(suc, u.f(suc, u.f(suc, zero)))), d_2_1_3,
    reference='2.1.3.3.a')

p_2_1_3_3_b = t.soet(fd_2_1_3_3_a, p_2_1_3_2_c, reference='2.1.3.3.b')

p_2_1_3_3_c = t.mp(
    t.commutativity_of_equality, fd_2_1_3_3_a, reference='2.1.3.3.c')

p_2_1_3_3_d = t.soet(p_2_1_3_3_c, p_2_1_3_2_c, reference='2.1.3.3.d')

p_2_1_4 = t.soet(p_2_2_5, p_2_1_3_3_c, reference='2.1.4')

t.nla(
    '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for every natural number n.',
    reference='2.3')

with u.v('n') as n:
    t.fa(
        valid_proposition=u.f(
            ft.implication(
                u.f(is_a, n, nat), u.f(ft.unequality, u.f(suc, n), zero))))

t.prnt()
