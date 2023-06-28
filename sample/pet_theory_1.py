import punctilious as pu

mira_name = 'Mira'  # random_data.random_word()
dog_name = 'dog'  # random_data.random_word()
mammal_name = 'mammal'  # random_data.random_word()

u = pu.UniverseOfDiscourse(dashed_name='The-world-of-Mira')
t1 = u.t(title=f'My pet theory')
mira = u.o.declare(pu.NameSet(mira_name))
dog = u.o.declare(pu.NameSet(dog_name))
mammal = u.o.declare(pu.NameSet(mammal_name))
is_a = u.r.declare(
    arity=2, formula_rep=pu.Formula.infix,
    symbol=pu.NameSet('is-a'),
    signal_proposition=True)
a1d = u.declare_axiom(f'{mira_name.capitalize()} is a {dog_name}.')
a1 = t1.include_axiom(a1d)
mira_is_a_dog = t1.i.axiom_interpretation.infer_statement(
    a1,
    u.f(is_a, mira, dog))

a2d = u.declare_axiom(f'If 𝒙 is a {dog_name}, then 𝒙 is a {mammal_name}.')
a2 = t1.include_axiom(a2d)
with u.v('x') as x:
    x_is_a_dog = u.f(is_a, x, dog)
    x_is_a_mammal = u.f(is_a, x, mammal)
    if_x_is_a_dog_then_x_is_a_mammal_formula = u.f(
        u.relations.implies, x_is_a_dog, x_is_a_mammal)
    if_x_is_a_dog_then_x_is_a_mammal = t1.i.axiom_interpretation.infer_statement(
        a2, if_x_is_a_dog_then_x_is_a_mammal_formula)
    # mira_is_a_mammal_formula = core.Formula(theory=t1, relation=is_a, parameters=(mira, mammal))

    vs = t1.i.vs.infer_statement(if_x_is_a_dog_then_x_is_a_mammal, mira)

    mira_is_a_mammal = t1.i.mp.infer_statement(
        vs,
        mira_is_a_dog)

t1.prnt()
