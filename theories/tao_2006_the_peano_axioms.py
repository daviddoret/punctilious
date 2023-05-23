import core

t = core.Theory(symbol=f'theory 2.1: the Peano axioms', capitalizable=True,
                extended_theories={core.foundation_theory})

nla_2_1_1 = t.nla(f'0 is a natural number.', symbol='2.1.1')
zero = t.o('0')
is_a = core.Relation(theory=t, symbol='is-a', arity=2, formula_rep=core.Formula.infix_operator_representation,
                     python_name='is_a', formula_is_proposition=True)
nat = t.o('natural-number', capitalizable=True)
fa_2_1_2 = core.FormalAxiom(
    theory=t, natural_language_axiom=nla_2_1_1, symbol='2.1.2',
    valid_proposition=core.Formula(theory=t, relation=is_a, parameters=(zero, nat)))

nla_2_2_1 = core.NaturalLanguageAxiom(
    theory=t, symbol='2.2.1',
    natural_language=f'If 𝐧 is a natural number, then 𝐧++ is a natural number.')
n = core.FreeVariable(theory=t, symbol='𝐧')
suc = core.Relation(theory=t, symbol='++', arity=1, formula_rep=core.Formula.postfix_operator_representation)
n_is_a_nat = core.Formula(theory=t, relation=is_a, parameters=(n, nat))
n_suc = core.Formula(theory=t, relation=suc, parameters=tuple([n]))
n_suc_is_a_nat = core.Formula(theory=t, relation=is_a, parameters=tuple([n_suc, nat]))
fa_2_2_1_formula = t.f(
    relation=core.implies,
    parameters=(n_is_a_nat, n_suc_is_a_nat))
fa_2_2_2 = core.FormalAxiom(
    theory=t, symbol='2.2.2', natural_language_axiom=nla_2_2_1,
    valid_proposition=fa_2_2_1_formula)

p_2_2_3 = core.ModusPonens(theory=t, symbol='2.2.3', p_implies_q=fa_2_2_2, p=fa_2_1_2)
p_2_2_4 = core.ModusPonens(theory=t, symbol='2.2.4', p_implies_q=fa_2_2_2, p=p_2_2_3)
p_2_2_5 = core.ModusPonens(theory=t, symbol='2.2.5', p_implies_q=fa_2_2_2, p=p_2_2_4)

d_2_1_3 = core.NaturalLanguageDefinition(
    theory=t, symbol='2.1.3',
    natural_language='We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number ((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text I use "x := y" to denote the statement that x is defined to equal y.)')

one = core.SimpleObjct(theory=t, symbol='1')
core.FormalDefinition(
    theory=t, symbol='2.1.3.1', natural_language_definition=d_2_1_3,
    valid_proposition=core.Formula(
        theory=t, relation=core.equality,
        parameters=(one, core.Formula(
            theory=t, relation=suc, parameters=(zero)))))

two = core.SimpleObjct(theory=t, symbol='2')
core.FormalDefinition(theory=t, symbol='2.1.3.2', natural_language_definition=d_2_1_3,
                      valid_proposition=core.Formula(theory=t, relation=core.equality, parameters=(two,
                                                                                                   core.Formula(
                                                                                                       theory=t,
                                                                                                       relation=suc,
                                                                                                       parameters=(
                                                                                                           one)))))

three = core.SimpleObjct(theory=t, symbol='3')
core.FormalDefinition(
    theory=t, symbol='2.1.3.3', natural_language_definition=d_2_1_3,
    valid_proposition=core.Formula(
        theory=t, relation=core.equality,
        parameters=(three,
                    core.Formula(theory=t, relation=suc, parameters=(two)))))

three_is_nat = core.Formula(theory=t, relation=is_a, parameters=(three, nat))
#####core.ModusPonens(theory=t1, symbol='2.1.4', p_implies_q=,


t.prnt()
