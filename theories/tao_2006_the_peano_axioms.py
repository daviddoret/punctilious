""""""
import punctilious as pu
import foundation_system_1 as fs1

# u = p.UniverseOfDiscourse()
# ft = u.t(
#    include_modus_ponens_inference_rule=True, include_conjunction_introduction_inference_rule=True,
#    include_double_negation_introduction_inference_rule=True)
# u = fs1.u
# ft = fs1.ft

pu.configuration.echo_default = True
pu.configuration.echo_axiom_inclusion = True
pu.configuration.echo_axiom_declaration = True
pu.configuration.echo_inferred_statement = True
pu.configuration.echo_simple_objct_declaration = True
pu.configuration.echo_statement = True
pu.configuration.echo_relation = True

pass

u = pu.UniverseOfDiscourse()

t = u.t(title=pu.Title(ref='2.1', subtitle='the Peano axioms'), extended_theory=fs1.ft)

section_2 = t.open_section('The natural numbers', section_number=2)

section_2_1 = t.open_section('The Peano axioms', section_parent=section_2)

# AXIOM 2.1.1
axiom_2_1_1_declaration = u.declare_axiom(f'0 is a natural number.')
axiom_2_1_1 = t.include_axiom(axiom_2_1_1_declaration, title='2.1.1')
zero = u.o.declare(pu.Symbol('0'))
natural_number = u.o.declare(pu.Symbol('natural-number'))
is_a = u.r.declare(2, pu.Symbol('is-a'), pu.Formula.infix, signal_proposition=True)
# (0 is-a natural-number):
proposition_2_1_1_1 = t.i.axiom_interpretation.infer_statement(
    axiom_2_1_1, u.f(is_a, zero, natural_number), title='2.1.1.1')

# AXIOM 2.1.2
axiom_2_1_2_declaration = u.declare_axiom('If n is a natural number, then n++ is a natural number.')
axiom_2_1_2 = t.include_axiom(axiom_2_1_2_declaration, title='2.1.2')
plusplus = u.r.declare(1, pu.Symbol('++'), formula_rep=pu.Formula.postfix, dashed_name='successor')
with u.v('n') as n:
    # ((n₁ is-a natural-number) ⟹ ((n₁)++ is-a natural-number)):
    proposition_2_1_2_1 = t.i.axiom_interpretation.infer_statement(
        axiom_2_1_2,
        u.f(u.r.implies, u.f(is_a, n, natural_number), u.f(is_a, u.f(plusplus, n), natural_number)),
        title='2.1.2.1')
# ((0 is-a natural-number) ⟹ ((0)++ is-a natural-number)):
proposition_2_1_2_2 = t.i.vs.infer_statement(proposition_2_1_2_1, zero, title='2.1.2.2')
# ((0)++ is-a natural-number):
proposition_2_1_2_3 = t.i.mp.infer_statement(proposition_2_1_2_2, proposition_2_1_1_1, title='2.2.3')

# DEFINITION 2.1.3
definition_2_1_3_declaration = u.declare_definition(
    'We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number '
    '((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text '
    'I use "x := y" to denote the statement that x is defined to equal y.)',
    title='2.1.3')
definition_2_1_3 = t.include_definition(d=definition_2_1_3_declaration)
one = u.o.declare(pu.Symbol('1'))
proposition_2_1_3_1 = t.i.definition_interpretation.infer_statement(
    definition_2_1_3, u.f(u.r.equal, one, u.f(plusplus, zero)), title='2.1.3.1')
two = u.o.declare(pu.Symbol('2'))
proposition_2_1_3_2 = t.i.definition_interpretation.infer_statement(
    definition_2_1_3, u.f(u.r.equal, two, u.f(plusplus, u.f(plusplus, zero))), title='2.1.3.2')
three = u.o.declare(pu.Symbol('3'))
proposition_2_1_3_3 = t.i.definition_interpretation.infer_statement(
    definition_2_1_3, u.f(u.r.equal, three, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero)))), title='2.1.3.3')
four = u.o.declare(pu.Symbol('4'))
proposition_2_1_3_4 = t.i.definition_interpretation.infer_statement(
    definition_2_1_3, u.f(u.r.equal, four, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero))))),
    title='2.1.3.4')

# RESUME CLEAN-UP FROM HERE

zero_plusplus = u.f(plusplus, zero)
p_2_2_4_1 = t.i.vs.infer_statement(proposition_2_1_2_1, zero_plusplus, title='2.2.3')
p_2_2_4 = t.i.mp.infer_statement(p_2_2_4_1, proposition_2_1_2_3, title='2.2.4')
zero_plus_plus_plusplus = u.f(plusplus, zero_plusplus)
p_2_2_5_1 = t.i.vs.infer_statement(proposition_2_1_2_1, zero_plus_plus_plusplus, title='2.2.3')
proposition_2_2_5 = t.i.mp.infer_statement(p_2_2_5_1, p_2_2_4, title='2.2.5')

proposition_2_1_3_100 = t.i.mp.infer_statement(
    t.commutativity_of_equality, proposition_2_1_3_1, title='2.1.3.1.b')

p_2_1_3_2_b = t.soet(
    proposition_2_1_3_2, proposition_2_1_3_100, reference='2.1.3.2.b')

p_2_1_3_2_c = t.i.mp.infer_statement(
    t.commutativity_of_equality, proposition_2_1_3_2, title='2.1.3.2.c')

p_2_1_3_2_d = t.soet(p_2_1_3_2_c, proposition_2_1_3_100, reference='2.1.3.2.d')

p_2_1_3_3_b = t.soet(proposition_2_1_3_3, p_2_1_3_2_c, reference='2.1.3.3.b')

p_2_1_3_3_c = t.i.mp.infer_statement(
    t.commutativity_of_equality, proposition_2_1_3_3, title='2.1.3.3.c')

p_2_1_3_3_d = t.soet(p_2_1_3_3_c, p_2_1_3_2_c, reference='2.1.3.3.d')

p_2_1_4 = t.soet(proposition_2_2_5, p_2_1_3_3_c, reference='2.1.4')

# 4
proposition_2_1_3_3 = t.i.definition_interpretation.infer_statement(
    definition_2_1_3,
    u.f(u.r.equal, four, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero))))),
    title='2.1.3.3.a')

# Axiom 2.3. 0 is not the successor of any natural number;
# i.e., we have n++ f=. 0 for every natural number n.

axiom_2_3 = t.include_axiom(u.declare_axiom(
    '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for '
    'every natural number n.'), title='2.3')

with u.v('n') as n:
    proposition_2_3_1 = t.i.axiom_interpretation.infer_statement(
        axiom_2_3,
        u.f(u.r.implies, u.f(is_a, n, natural_number), u.f(u.r.neq, u.f(plusplus, n), zero)),
        title='2.3.1'
    )


# Proposition 2.1.6. 4 is not equal to 0.
def prove_proposition_2_1_6():
    p1 = t.i.mp.infer_statement(proposition_2_3_1, proposition_2_2_5, title='2.1.6.1')
    p2 = t.i.mp.infer_statement(
        ft.commutativity_of_equality, proposition_2_1_3_3, title='2.1.6.2')
    p3 = t.soet(p1, p2, reference='2.1.6.3')
    pass


prove_proposition_2_1_6()
axiom_2_4 = t.include_axiom(u.declare_axiom(
    'Different natural numbers must have different successors; i.e., if n, '
    'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
    'if n++ = m++, then we must have n = m.'), title='2.4')

with u.v('n') as n, u.v('m') as m:
    proposition_2_4_1 = t.i.axiom_interpretation.infer_statement(
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
            u.f(u.r.neq, u.f(plusplus, n), u.f(plusplus, m)))
        , title='2.4.1')

# Proposition 2.1.8: 6 is not equal to 2.


# t.prnt(output_proofs=True)
