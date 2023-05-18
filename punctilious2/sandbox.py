import core
import random_data

mira_name = 'Mira'  # random_data.random_word()
dog_name = 'dog'  # random_data.random_word()
mammal_name = 'mammal'  # random_data.random_word()
#n4 = random_data.random_word()
#n5 = random_data.random_word()

t1 = core.Theory(symbol=f'{mira_name}-theory', capitalizable=True)
mira = core.SimpleObjct(theory=t1, symbol=mira_name, capitalizable=True)
dog = core.SimpleObjct(theory=t1, symbol=dog_name, capitalizable=True)
mammal = core.SimpleObjct(theory=t1, symbol=mammal_name, capitalizable=True)
is_a = core.Relation(theory=t1, arity=2, formula_rep=core.Formula.reps.infix_operator, symbol='is-a', python_name='is_a')

a1 = core.Axiom(theory=t1, axiom_text=f'{mira_name.capitalize()} is a {dog_name}.', capitalizable=True)
mira_is_a_dog = core.DirectAxiomInferenceStatement(theory=t1, axiom=a1, valid_proposition=core.Formula(theory=t1, relation=is_a, parameters=(mira, dog)))

a2 = core.Axiom(theory=t1, axiom_text=f'If a 𝒙 is a {dog_name}, then 𝒙 is a {mammal_name}.', capitalizable=True)
x_is_a_dog = core.Formula(theory=t1, relation=is_a, parameters=(core.FreeVariablePlaceholder(symbol='𝒙'), dog))
x_is_a_mammal = core.Formula(theory=t1, relation=is_a, parameters=(core.FreeVariablePlaceholder(symbol='𝒙'), mammal))
if_x_is_a_dog_then_x_is_a_mammal_formula = core.Formula(theory=t1, relation=core.propositional_logic.relations.implies, parameters=(x_is_a_dog, x_is_a_mammal))
if_x_is_a_dog_then_x_is_a_mammal = core.DirectAxiomInferenceStatement(theory=t1, axiom=a1, valid_proposition=if_x_is_a_dog_then_x_is_a_mammal_formula)
# mira_is_a_mammal_formula = core.Formula(theory=t1, relation=is_a, parameters=(mira, mammal))

mira_is_a_mammal = core.ModusPonensStatement(theory=t1, p_implies_q=if_x_is_a_dog_then_x_is_a_mammal, p_is_true=mira_is_a_dog)

t1.prnt()

