import core
import random_data

t1 = core.Theory(symbol=f'theory 2.1: the Peano axioms', capitalizable=True,
                 extended_theories={core.foundation_theory})

axiom_2_1 = core.FreeTextAxiom(theory=t1, symbol='axiom 2.1', axiom_text=f'0 is a natural number.', capitalizable=True)
zero = core.SimpleObjct(theory=t1, symbol='0', capitalizable=True)
is_a = core.Relation(theory=t1, symbol='is-a', arity=2, formula_rep=core.Formula.infix_operator_representation,
                     python_name='is_a', formula_is_proposition=True)
nat = core.SimpleObjct(theory=t1, symbol='natural-number', capitalizable=True)
zero_is_a_nat = core.FormalAxiom(
    theory=t1, axiom=axiom_2_1,
    valid_proposition=core.Formula(theory=t1, relation=is_a, parameters=(zero, nat)))

axiom_2_2 = core.FreeTextAxiom(theory=t1, symbol='axiom 2.2',
                               axiom_text=f'If 𝐧 is a natural number, then 𝐧++ is a natural number.',
                               capitalizable=True)
n = core.FreeVariable(theory=t1, symbol='𝐧')
suc = core.Relation(theory=t1, symbol='++', arity=1, formula_rep=core.Formula.postfix_operator_representation)
n_is_a_nat = core.Formula(theory=t1, relation=is_a, parameters=(n, nat))
n_suc = core.Formula(theory=t1, relation=suc, parameters=tuple([n]))
n_suc_is_a_nat = core.Formula(theory=t1, relation=is_a, parameters=tuple([n_suc, nat]))
if_n_is_a_nat_then_n_suc_is_a_nat = core.Formula(
    theory=t1, relation=core.foundation_theory.relations.implies,
    parameters=(n_is_a_nat, n_suc_is_a_nat))
if_n_is_a_nat_then_n_suc_is_a_nat = core.FormalAxiom(
    theory=t1, axiom=axiom_2_2,
    valid_proposition=if_n_is_a_nat_then_n_suc_is_a_nat)

p1 = core.ModusPonens(theory=t1, p_implies_q=if_n_is_a_nat_then_n_suc_is_a_nat, p=zero_is_a_nat)

p2 = core.ModusPonens(theory=t1, p_implies_q=if_n_is_a_nat_then_n_suc_is_a_nat, p=p1)

p3 = core.ModusPonens(theory=t1, p_implies_q=if_n_is_a_nat_then_n_suc_is_a_nat, p=p2)

d_2_1_3 = core.FreeTextDefinition(theory=t1, symbol='definition 2.1.3',
                                  text='We define 1 to be the number 0++, 2 to be the number (0++)++, 3 to be the number ((0++)++)++,etc. (In other words, 1 := 0++, 2 := 1++, 3 := 2++, etc. In this text I use "x := y" to denote the statement that xis defined to equal y.)',
                                  capitalizable=True)

one = core.SimpleObjct(theory=t1, symbol='1')
core.FormalDefinition(theory=t1, free_text_definition=d_2_1_3,
                      valid_proposition=core.Formula(theory=t1, relation=core.equality, parameters=(one,
                                                                                                    core.Formula(
                                                                                                        theory=t1,
                                                                                                        relation=suc,
                                                                                                        parameters=(
                                                                                                            zero)))))

two = core.SimpleObjct(theory=t1, symbol='2')
core.FormalDefinition(theory=t1, free_text_definition=d_2_1_3,
                      valid_proposition=core.Formula(theory=t1, relation=core.equality, parameters=(two,
                                                                                                    core.Formula(
                                                                                                        theory=t1,
                                                                                                        relation=suc,
                                                                                                        parameters=(
                                                                                                            one)))))

three = core.SimpleObjct(theory=t1, symbol='3')
core.FormalDefinition(theory=t1, free_text_definition=d_2_1_3,
                      valid_proposition=core.Formula(theory=t1, relation=core.equality, parameters=(three,
                                                                                                    core.Formula(
                                                                                                        theory=t1,
                                                                                                        relation=suc,
                                                                                                        parameters=(
                                                                                                            two)))))

t1.prnt()
