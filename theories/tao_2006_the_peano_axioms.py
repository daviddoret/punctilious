import core

t = core.Theory(
    symbol=f'theory 2.1: the Peano axioms', capitalizable=True,
    extended_theories={core.foundation_theory})

# simple-objct declarations
zero = t.o('0')
one = t.o('1')
two = t.o('2')
three = t.o('3')
nat = t.o('natural-number', capitalizable=True)

# relation declarations
is_a = t.r(
    2, 'is-a', core.Formula.infix_operator_representation,
    python_name='is_a', signal_proposition=True)

nla_2_1 = t.nla(f'0 is a natural number.', symbol='2.1')
fa_2_1_a = t.fa(t.f(is_a, zero, nat), nla_2_1, symbol='2.1.a')

nla_2_2_1 = t.nla(
    'If 𝐧 is a natural number, then 𝐧++ is a natural number.', symbol='2.2.1')
n = t.v('𝐧')
suc = t.r(1, '++', formula_rep=core.Formula.postfix_operator_representation)
fa_2_2_2 = t.fa(
    t.f(core.implies, t.f(is_a, n, nat), t.f(is_a, t.f(suc, n), nat)),
    nla_2_2_1,
    symbol='2.2.2')

p_2_2_3 = t.mp(fa_2_2_2, fa_2_1_a, symbol='2.2.3')
p_2_2_4 = t.mp(fa_2_2_2, p_2_2_3, symbol='2.2.4')
p_2_2_5 = t.mp(fa_2_2_2, p_2_2_4, symbol='2.2.5')

d_2_1_3 = t.nld(
    'We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
    '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
    'I use "x := y" to denote the statement that x is defined to equal y.)',
    symbol='2.1.3')

fd_2_1_3_a = t.fd(
    t.f(core.equality, one, t.f(suc, zero)), d_2_1_3, symbol='2.1.3.a')
fd_2_1_3_b = t.fd(
    t.f(core.equality, two, t.f(suc, t.f(suc, zero))), d_2_1_3,
    symbol='2.1.3.b')
fd_2_1_3_c = t.fd(
    t.f(core.equality, three, t.f(suc, t.f(suc, t.f(suc, zero)))), d_2_1_3,
    symbol='2.1.3.c')

fd_2_1_3_d = t.fd(
    t.f(core.equality, two, t.f(suc, one)), d_2_1_3, symbol='2.1.3.d')
fd_2_1_3_e = t.fd(
    t.f(core.equality, three, t.f(suc, two)), d_2_1_3, symbol='2.1.3.e')

fd_2_1_3_c = t.mp(
    core.commutativity_of_equality, fd_2_1_3_c, symbol='2.1.3.c.2')

t.soet(p_2_2_5, fd_2_1_3_c, symbol='2.1.3.c.3')

#####core.ModusPonens(theory=t1, symbol='2.1.4', p_implies_q=,


t.prnt()
