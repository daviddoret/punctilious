import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.create_universe_of_discourse(echo=True)
a1 = u.a.declare(natural_language='Dummy axiom to establish some ground propositions.')
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
r1 = u.c1.declare()
r2 = u.c1.declare()
phi1 = o1 | r1 | o2
phi2 = o3 | r2 | phi1
const1 = u.c3.declare(value=o2)
const2 = u.c3.declare(value=phi2)
with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
    phi3 = (phi2 | r2 | y) | r1 | (x | r2 | (const2 | r1 | (y | r1 | const1)))

output1 = tuple(pu.iterate_formula_data_model_components(u=u, phi=o1, recurse_constant_value=True,
    recurse_compound_formula_connective=True, recurse_compound_formula_terms=True, recurse_statement_proposition=True,
    yield_classes=None))
print(f'output1: {output1}')

output2 = tuple(pu.iterate_formula_data_model_components(u=u, phi=phi1, recurse_constant_value=True,
    recurse_compound_formula_connective=True, recurse_compound_formula_terms=True, recurse_statement_proposition=True,
    yield_classes=None))
print(f'output2: {output2}')

output3 = tuple(pu.iterate_formula_data_model_components(u=u, phi=phi2, recurse_constant_value=True,
    recurse_compound_formula_connective=True, recurse_compound_formula_terms=True, recurse_statement_proposition=True,
    yield_classes=None))
print(f'output3: {output3}')

output4 = tuple(pu.iterate_formula_data_model_components(u=u, phi=phi2, recurse_constant_value=True,
    recurse_compound_formula_connective=True, recurse_compound_formula_terms=True, recurse_statement_proposition=True,
    yield_classes=(pu.Connective)))
print(f'output4: {output4}')

output5 = tuple(pu.iterate_formula_data_model_components(u=u, phi=phi3, recurse_constant_value=True,
    recurse_compound_formula_connective=True, recurse_compound_formula_terms=True, recurse_statement_proposition=True,
    yield_classes=(pu.Connective, pu.FreeVariable)))
print(f'output5: {output5}')

output6 = tuple(pu.iterate_formula_data_model_components(u=u, phi=phi3, recurse_constant_value=True,
    recurse_compound_formula_connective=False, recurse_compound_formula_terms=True, recurse_statement_proposition=True,
    yield_classes=(pu.Connective, pu.FreeVariable)))
print(f'output6: {output6}')

output7 = tuple(pu.iterate_formula_data_model_components(u=u, phi=phi3, recurse_constant_value=True,
    recurse_compound_formula_connective=True, recurse_compound_formula_terms=False, recurse_statement_proposition=True,
    yield_classes=(pu.Connective, pu.FreeVariable)))
print(f'output7: {output7}')

output8 = tuple(
    pu.iterate_formula_data_model_components(u=u, phi=phi3, yield_parent_constant=False, recurse_constant_value=True,
        recurse_compound_formula_connective=True, recurse_compound_formula_terms=False,
        recurse_statement_proposition=True, yield_classes=(pu.Connective, pu.FreeVariable)))
print(f'output8: {output8}')
