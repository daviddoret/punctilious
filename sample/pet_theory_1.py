import core
import random_data

mira_name = 'Mira'  # random_data.random_word()
dog_name = 'dog'  # random_data.random_word()
mammal_name = 'mammal'  # random_data.random_word()

t1 = core.TheoryElaborationSequence(symbol=f'pet-theory-1', capitalizable=True)
mira = core.SimpleObjct(theory=t1, symbol=mira_name, capitalizable=True)
dog = core.SimpleObjct(theory=t1, symbol=dog_name, capitalizable=True)
mammal = core.SimpleObjct(theory=t1, symbol=mammal_name, capitalizable=True)
is_a = core.Relation(
    theory=t1, arity=2, formula_rep=core.Formula.infix,
    symbol='is-a',
    python_name='is_a', signal_proposition=True)

a1 = core.AxiomInclusion(
    t=t1, natural_language=f'{mira_name.capitalize()} is a {dog_name}.',
    capitalizable=True)
mira_is_a_dog = core.DirectAxiomInference(
    theory=t1, ap=a1,
    valid_proposition=core.Formula(
        theory=t1, relation=is_a, parameters=(mira, dog)))

a2 = core.AxiomInclusion(
    t=t1,
    natural_language=f'If 𝒙 is a {dog_name}, then 𝒙 is a {mammal_name}.',
    capitalizable=True)
x = core.FreeVariable(theory=t1)
x_is_a_dog = core.Formula(theory=t1, relation=is_a, parameters=(x, dog))
x_is_a_mammal = core.Formula(theory=t1, relation=is_a, parameters=(x, mammal))
if_x_is_a_dog_then_x_is_a_mammal_formula = core.Formula(
    theory=t1, relation=core.foundation_theory.relations.implies,
    parameters=(x_is_a_dog, x_is_a_mammal))
if_x_is_a_dog_then_x_is_a_mammal = core.DirectAxiomInference(
    theory=t1, ap=a2,
    valid_proposition=if_x_is_a_dog_then_x_is_a_mammal_formula)
# mira_is_a_mammal_formula = core.Formula(theory=t1, relation=is_a, parameters=(mira, mammal))

x = mira_is_a_dog.valid_proposition.is_masked_formula_similar_to(
    x_is_a_dog, mask={x})

mira_is_a_mammal = core.ModusPonens(
    theory=t1, conditional=if_x_is_a_dog_then_x_is_a_mammal,
    antecedent=mira_is_a_dog)

t1.prnt()
