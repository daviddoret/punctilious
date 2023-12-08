from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestVariableSubstitution(TestCase):

    def test_variable_substitution_without_variable(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.c1.declare(arity=1, signal_proposition=True)
        r2 = u.c1.declare(arity=2, signal_proposition=True)
        t = u.t.declare()
        a = u.a.declare(natural_language=random_data.random_sentence())
        ap = t.include_axiom(a=a)
        p_formula = r1(r2(o1, o2))
        p_statement = t.i.axiom_interpretation.infer_formula_statement(a=ap, p=p_formula, echo=True)
        # y_sequence = tuple()
        p_prime = t.i.vs.infer_formula_statement(p=p_statement, phi=u.c1.tupl(), echo=True)
        self.assertTrue(p_prime.is_formula_syntactically_equivalent_to(phi=p_statement))
        self.assertEqual('𝑟₁(𝑟₂(𝑜₁, 𝑜₂))', p_prime.rep_formula(encoding=pu.encodings.unicode))

    def test_variable_substitution_with_variables(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        o4 = u.o.declare()
        o5 = u.o.declare()
        o6 = u.o.declare()
        f = u.c1.declare(arity=1, signal_proposition=True, symbol='f', auto_index=False)
        g = u.c1.declare(arity=2, signal_proposition=True, symbol='g', auto_index=False)
        t = u.t.declare()
        a = u.a.declare(random_data.random_sentence())
        ap = t.include_axiom(a)
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y',
            auto_index=False) as y, u.with_variable(symbol='z', auto_index=False) as z:
            p_statement = t.i.axiom_interpretation.infer_formula_statement(a=ap, p=f(g(g(z, g(f(x), y)), g(x, y))),
                echo=True)
        self.assertEqual('𝑓(𝑔(𝑔(𝐳, 𝑔(𝑓(𝐱), 𝐲)), 𝑔(𝐱, 𝐲)))', p_statement.rep_formula(encoding=pu.encodings.unicode))
        p_prime = t.i.vs.infer_formula_statement(p=p_statement, phi=u.c1.tupl(o4, o6, o5), echo=True)
        self.assertEqual('𝑓(𝑔(𝑔(𝑜₄, 𝑔(𝑓(𝑜₆), 𝑜₅)), 𝑔(𝑜₆, 𝑜₅)))', p_prime.rep_formula(encoding=pu.encodings.unicode))
        p_prime.is_formula_syntactically_equivalent_to(phi=f(g(g(o4, g(f(o6), o5)), g(o6, o5))))
