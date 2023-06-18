""""""
import punctilious as pu
import foundation_system_1 as fs1

# u = p.UniverseOfDiscourse()
# ft = u.t(
#    include_modus_ponens_inference_rule=True, include_conjunction_introduction_inference_rule=True,
#    include_double_negation_introduction_inference_rule=True)
u = fs1.u
ft = fs1.ft

t = u.t(
    header=f'theory 2.1: the Peano axioms',
    extended_theory=fs1.ft, dashed_name='tao-2006-theory-2-1-the-peano-axioms')

# simple-objct declarations
zero = u.o.declare('0')
one = u.o.declare('1')
two = u.o.declare('2')
three = u.o.declare('3')
four = u.o.declare('4')
nat = u.o.declare('natural-number')

# relation declarations
is_a = u.r.declare(
    2, 'is-a', pu.Formula.infix_operator_representation,
    signal_proposition=True)

nla_2_1 = t.postulate_axiom(u.elaborate_axiom(f'0 is a natural number.'), header='2.1')
fa_2_1_a = t.dai(u.f(is_a, zero, nat), nla_2_1, header='2.1.a')

nla_2_2_1 = t.postulate_axiom(u.elaborate_axiom(
    'If n is a natural number, then n++ is a natural number.'), header='2.2.1')
with u.v('n') as n:
    suc = u.r.declare(1, '++', formula_rep=pu.Formula.postfix_operator_representation, dashed_name='successor')
    fa_2_2_2 = t.dai(
        u.f(u.r.implies, u.f(is_a, n, nat), u.f(is_a, u.f(suc, n), nat)),
        nla_2_2_1,
        header='2.2.2')

p_2_2_3 = t.i.mp.infer_statement(fa_2_2_2, fa_2_1_a, header='2.2.3')
p_2_2_4 = t.i.mp.infer_statement(fa_2_2_2, p_2_2_3, header='2.2.4')
proposition_2_2_5 = t.i.mp.infer_statement(fa_2_2_2, p_2_2_4, header='2.2.5')

# Definition 2.1.3. We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number ((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text I use "x := y" to denote the statement that xis defined to equal y.)

def_2_1_3 = u.pose_definition(
    'We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
    '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
    'I use "x := y" to denote the statement that x is defined to equal y.)',
    header='2.1.3')
definition_2_1_3 = t.endorse_definition(d=def_2_1_3)

# 1
proposition_2_1_3_1 = t.ddi(
    u.f(u.r.eq, one, u.f(suc, zero)), definition_2_1_3,
    header='2.1.3.1')

# 2
proposition_2_1_3_2 = t.ddi(
    u.f(u.r.eq, two, u.f(suc, u.f(suc, zero))), definition_2_1_3,
    header='2.1.3.2')

# 3
proposition_2_1_3_3 = t.ddi(
    u.f(u.r.eq, three, u.f(suc, u.f(suc, u.f(suc, zero)))),
    definition_2_1_3,
    header='2.1.3.3')

proposition_2_1_3_100 = t.i.mp.infer_statement(
    t.commutativity_of_equality, proposition_2_1_3_1, header='2.1.3.1.b')

p_2_1_3_2_b = t.soet(
    proposition_2_1_3_2, proposition_2_1_3_100, reference='2.1.3.2.b')

p_2_1_3_2_c = t.i.mp.infer_statement(
    t.commutativity_of_equality, proposition_2_1_3_2, header='2.1.3.2.c')

p_2_1_3_2_d = t.soet(p_2_1_3_2_c, proposition_2_1_3_100, reference='2.1.3.2.d')

p_2_1_3_3_b = t.soet(proposition_2_1_3_3, p_2_1_3_2_c, reference='2.1.3.3.b')

p_2_1_3_3_c = t.i.mp.infer_statement(
    t.commutativity_of_equality, proposition_2_1_3_3, header='2.1.3.3.c')

p_2_1_3_3_d = t.soet(p_2_1_3_3_c, p_2_1_3_2_c, reference='2.1.3.3.d')

p_2_1_4 = t.soet(proposition_2_2_5, p_2_1_3_3_c, reference='2.1.4')

# 4
proposition_2_1_3_3 = t.ddi(
    u.f(u.r.eq, four, u.f(suc, u.f(suc, u.f(suc, u.f(suc, zero))))),
    definition_2_1_3,
    header='2.1.3.3.a')

# Axiom 2.3. 0 is not the successor of any natural number;
# i.e., we have n++ f=. 0 for every natural number n.

a_2_3 = t.postulate_axiom(u.elaborate_axiom(
    '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for '
    'every natural number n.'), header='2.3')

with u.v('n') as n:
    proposition_2_3_1 = t.dai(
        valid_proposition=u.f(
            u.r.implies,
            u.f(is_a, n, nat),
            u.f(u.r.neq, u.f(suc, n), zero)),
        ap=a_2_3, header='2.3.1')


# Proposition 2.1.6. 4 is not equal to 0.
def prove_proposition_2_1_6():
    p1 = t.i.mp.infer_statement(proposition_2_3_1, proposition_2_2_5, header='2.1.6.1')
    p2 = t.i.mp.infer_statement(
        ft.commutativity_of_equality, proposition_2_1_3_3, header='2.1.6.2')
    p3 = t.soet(p1, p2, reference='2.1.6.3')
    pass


prove_proposition_2_1_6()
axiom_2_4 = t.postulate_axiom(u.elaborate_axiom(
    'Different natural numbers must have different successors; i.e., if n, '
    'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
    'if n++ = m++, then we must have n = m.'), header='2.4')

with u.v('n') as n, u.v('m') as m:
    proposition_2_4_1 = t.dai(
        u.f(
            u.r.implies,
            u.f(
                u.r.land,
                u.f(
                    u.r.land,
                    u.f(is_a, n, nat),
                    u.f(is_a, m, nat)),
                u.f(u.r.neq, n, m)),
            u.f(u.r.neq, u.f(suc, n), u.f(suc, m)))
        , header='2.4.1', ap=axiom_2_4)

# Proposition 2.1.8: 6 is not equal to 2.


# t.prnt(output_proofs=True)
