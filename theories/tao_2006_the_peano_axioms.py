""""""
import punctilious as pu

pu.configuration.echo_default = True
pu.configuration.echo_axiom_declaration = True
pu.configuration.echo_axiom_inclusion = True
pu.configuration.echo_definition_declaration = True
pu.configuration.echo_definition_inclusion = True
pu.configuration.echo_inferred_statement = True
pu.configuration.echo_proof = False
pu.configuration.echo_simple_objct_declaration = True
pu.configuration.echo_statement = True
pu.configuration.echo_relation = True

pass

u = pu.UniverseOfDiscourse()

# SECTION 2.1

t = u.t(ref='2.1', subtitle='the Peano axioms')

section_2 = t.open_section('The natural numbers', section_number=2)

section_2_1 = t.open_section('The Peano axioms', section_parent=section_2)

# AXIOM 2.1.1

a01 = u.declare_axiom(f'0 is a natural number.')
a02 = t.include_axiom(a01, ref='2.1.1')
zero = u.o.declare(symbol='0', auto_index=False)
natural_number = u.o.declare(symbol='natural-number', auto_index=False)
is_a = u.r.declare(arity=2, symbol='is-a', auto_index=False, formula_rep=pu.Formula.infix,
                   signal_proposition=True)
# (0 is-a natural-number):
p001 = t.i.axiom_interpretation.infer_statement(a02, u.f(is_a, zero, natural_number))

# AXIOM 2.1.2

a03 = u.declare_axiom('If n is a natural number, then n++ is a natural number.')
a04 = t.include_axiom(a03, ref='2.1.2')
plusplus = u.r.declare(arity=1, symbol='++', auto_index=False, name='successor',
                       formula_rep=pu.Formula.postfix)
with u.v('n') as n:
    # ((n₁ is-a natural-number) ⟹ ((n₁)++ is-a natural-number)):
    p002 = t.i.axiom_interpretation.infer_statement(
        a04,
        u.f(u.r.implies, u.f(is_a, n, natural_number), u.f(is_a, u.f(plusplus, n), natural_number)))
# ((0 is-a natural-number) ⟹ ((0)++ is-a natural-number)):
p003 = t.i.variable_substitution.infer_statement(p002, zero)
# ((0)++ is-a natural-number):
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
p009 = t.i.variable_substitution.infer_statement(p002, zero_plusplus, ref='2.2.3')
p010 = t.i.mp.infer_statement(p009, p004, ref='2.2.4')
zero_plus_plus_plusplus = u.f(plusplus, zero_plusplus)
p011 = t.i.variable_substitution.infer_statement(p002, zero_plus_plus_plusplus, ref='2.2.3')
p012 = t.i.mp.infer_statement(p011, p010, ref='2.2.5')
zero_plus_plus_plus_plusplus = u.f(plusplus, zero_plus_plus_plusplus)
p013 = t.i.variable_substitution.infer_statement(p002, zero_plus_plus_plus_plusplus, ref='2.2.3')
p014 = t.i.mp.infer_statement(p013, p012, ref='2.2.5')
p015 = t.i.equality_commutativity.infer_statement(p005)
p016 = t.i.equal_terms_substitution.infer_statement(p006, p015)
p017 = t.i.equality_commutativity.infer_statement(p006)
p018 = t.i.equal_terms_substitution.infer_statement(p017, p015)
p019 = t.i.equal_terms_substitution.infer_statement(p007, p017)
p020 = t.i.equality_commutativity.infer_statement(p007)
p021 = t.i.equal_terms_substitution.infer_statement(p020, p017)
p022 = t.i.equal_terms_substitution.infer_statement(p012, p020)
p023 = t.i.definition_interpretation.infer_statement(
    d02, u.f(u.r.equal, four, u.f(plusplus, u.f(plusplus, u.f(plusplus, u.f(plusplus, zero))))))
p024 = t.i.equality_commutativity.infer_statement(p008)
p025 = t.i.equal_terms_substitution.infer_statement(p024, p020)
p026 = t.i.equal_terms_substitution.infer_statement(p013, p025)

a05 = t.include_axiom(u.declare_axiom(
    '0 is not the successor of any natural number; i.e., we have n++ ≠ 0 for '
    'every natural number n.'), ref='2.3')

with u.v('n') as n:
    p027 = t.i.axiom_interpretation.infer_statement(
        a05, u.f(u.r.implies, u.f(is_a, n, natural_number), u.f(u.r.neq, u.f(plusplus, n), zero)),
        ref='2.3.1')

# Proposition 2.1.6. 4 is not equal to 0.
t.take_note('We want to prove that 4 is not equal to 0, i.e. (4 ≠ 0).')
p028 = t.i.variable_substitution.infer_statement(p027, three)
p029 = t.i.modus_ponens.infer_statement(p028, p022)
p030 = t.i.equal_terms_substitution.infer_statement(p029, p025, ref='2.1.6')

axiom_2_4 = t.include_axiom(u.declare_axiom(
    'Different natural numbers must have different successors; i.e., if n, '
    'm are natural numbers and n ≠ m, then n++ ≠ m++. Equivalently, '
    'if n++ = m++, then we must have n = m.'), ref='2.4')

with u.v('n') as n, u.v('m') as m:
    p031 = t.i.axiom_interpretation.infer_statement(
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
        , ref='2.4.1')
