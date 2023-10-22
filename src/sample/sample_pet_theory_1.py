import punctilious as pu

mira_name = 'Mira'  # random_data.random_word()
dog_name = 'dog'  # random_data.random_word()
mammal_name = 'mammal'  # random_data.random_word()

u = pu.UniverseOfDiscourse(dashed_name='The-world-of-Mira')
t1 = u.t()
mira = u.o.declare(symbol=mira_name, auto_index=False)
dog = u.o.declare(symbol=dog_name, auto_index=False)
mammal = u.o.declare(symbol=mammal_name, auto_index=False)
a1d = u.declare_axiom(natural_language=f'{mira_name.capitalize()} is a {dog_name}.')
a1 = t1.include_axiom(a=a1d)
mira_is_a_dog = t1.i.axiom_interpretation.infer_formula_statement(a=a1, p=mira | u.r.is_a | dog)

a2d = u.declare_axiom(natural_language=f'If 𝒙 is a {dog_name}, then 𝒙 is a {mammal_name}.')
a2 = t1.include_axiom(a=a2d)
with u.with_variable('x') as x:
    x_is_a_dog = x | u.r.is_a | dog
    x_is_a_mammal = x | u.r.is_a | mammal
    if_x_is_a_dog_then_x_is_a_mammal_formula = x_is_a_dog | u.relations.implies | x_is_a_mammal
    if_x_is_a_dog_then_x_is_a_mammal = t1.i.axiom_interpretation.infer_formula_statement(a=a2,
        p=if_x_is_a_dog_then_x_is_a_mammal_formula)
    # mira_is_a_mammal_formula = core.Formula(theory=t1, relation=is_a, parameters=(mira, mammal))

    vs = t1.i.vs.infer_formula_statement(p=if_x_is_a_dog_then_x_is_a_mammal, phi=u.r.tupl(mira))

    mira_is_a_mammal = t1.i.mp.infer_formula_statement(p_implies_q=vs, p=mira_is_a_dog)

t1.prnt()
