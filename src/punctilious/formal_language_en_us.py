import typing
import typesetting as ts
import formal_language as fl

ts.register_styledstring(python_type=fl.MetaLanguage, text="meta-language", treatment=ts.treatments.default,
    flavor=ts.flavors.default, language=ts.languages.default)

ts.register_styledstring(python_type=fl.MetaLanguageClassAccretor, text="classes", treatment=ts.treatments.default,
    flavor=ts.flavors.default, language=ts.languages.default)

# y = fl.FormalObject()  # print(y.to_string(protocol=ts.protocols.unicode_extended))
# print(y.to_string(protocol=ts.protocols.latex))
# print(y.to_string(protocol=ts.protocols.unicode_extended))
# print(y.to_string(protocol=ts.protocols.unicode_limited))
# print(y)

# y = fl.MetaLanguageClassAccretor()  # print(y.to_string(protocol=ts.protocols.unicode_extended))
# print(y.to_string(protocol=ts.protocols.latex))
# print(y.to_string(protocol=ts.protocols.unicode_extended))
# print(y.to_string(protocol=ts.protocols.unicode_limited))
# print(y)

pass
