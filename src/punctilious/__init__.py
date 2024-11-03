import punctilious as pu

formats = pu.Formats()
representation_methods = pu.RepresentationMethods()
symbols = pu.Symbols()
connectors = pu.get_connectors()

print(symbols.p_uppercase_serif_italic_1.rep(formats.latex_math_1))
print(symbols.q_uppercase_serif_italic_1.rep(formats.unicode_1))
print(symbols.r_uppercase_serif_italic_1.rep(formats.unicode_2))
print(symbols.r_uppercase_serif_italic_1.rep(formats.technical_1))

print(connectors.conjunction_1.rep(
    args=(symbols.p_uppercase_serif_italic_1, symbols.q_uppercase_serif_italic_1),
    format=formats.unicode_1))
print(connectors.is_a_proposition_predicate_1.unicode_1_template)
