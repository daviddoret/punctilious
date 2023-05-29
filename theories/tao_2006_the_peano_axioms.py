import punctilious as pu

t = pu.Theory(
    symbol=f'theory 2.1: the Peano axioms', capitalizable=True,
    extended_theories={pu.ft})

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

# 1
fd_2_1_3_1_a = t.fd(
    t.f(core.equality, one, t.f(suc, zero)), d_2_1_3, symbol='2.1.3.1.a')

p_2_1_3_1_b = t.mp(
    core.commutativity_of_equality, fd_2_1_3_1_a, symbol='2.1.3.1.b')

# 2
fd_2_1_3_2_a = t.fd(
    t.f(core.equality, two, t.f(suc, t.f(suc, zero))), d_2_1_3,
    symbol='2.1.3.2.a')
p_2_1_3_2_b = t.soet(fd_2_1_3_2_a, p_2_1_3_1_b, symbol='2.1.3.2.b')

p_2_1_3_2_c = t.mp(
    core.commutativity_of_equality, fd_2_1_3_2_a, symbol='2.1.3.2.c')

p_2_1_3_2_d = t.soet(p_2_1_3_2_c, p_2_1_3_1_b, symbol='2.1.3.2.d')

# 3
fd_2_1_3_3_a = t.fd(
    t.f(core.equality, three, t.f(suc, t.f(suc, t.f(suc, zero)))), d_2_1_3,
    symbol='2.1.3.3.a')

p_2_1_3_3_b = t.soet(fd_2_1_3_3_a, p_2_1_3_2_c, symbol='2.1.3.3.b')

p_2_1_3_3_c = t.mp(
    core.commutativity_of_equality, fd_2_1_3_3_a, symbol='2.1.3.3.c')

p_2_1_3_3_d = t.soet(p_2_1_3_3_c, p_2_1_3_2_c, symbol='2.1.3.3.d')

p_2_1_4 = t.soet(p_2_2_5, p_2_1_3_3_c, symbol='2.1.4')

t.nla(
    '0 is not the successor of any natural number; i.e., we have n++ f=. 0 for every natural number n',
    symbol='2.3')

t.prnt()
