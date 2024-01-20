import typing
import typesetting as ts
import formal_language
import pl1

ts.register_symbol(python_type=pl1.Negation, symbol=ts.symbols.not_sign, treatment=ts.treatments.default,
    flavor=ts.flavors.default, language=ts.languages.default)
ts.register_symbol(python_type=pl1.MaterialImplication, symbol=ts.symbols.rightwards_arrow,
    treatment=ts.treatments.default, flavor=ts.flavors.default, language=ts.languages.default)

y = pl1.MaterialImplication()  # print(y.to_string(protocol=ts.protocols.unicode_extended))
print(y.to_string(protocol=ts.protocols.latex))
print(y.to_string(protocol=ts.protocols.unicode_extended))
print(y.to_string(protocol=ts.protocols.unicode_limited))
print(y)

x = pl1.Negation()
print(x)
print(x.to_string(protocol=ts.protocols.latex))
print(x.to_string(protocol=ts.protocols.unicode_extended))

pass
