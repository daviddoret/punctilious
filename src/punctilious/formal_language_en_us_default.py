import typing

import formal_language_tags
import typesetting as ts
import formal_language_tags as fl_tags

flavor: ts.Flavor = ts.flavors.default
language: ts.Language = ts.languages.en_us

ts.register_symbol(tag=fl_tags.connective, symbol=ts.symbols.asterisk_operator,
    treatment=ts.treatments.symbolic_representation, flavor=flavor, language=language)

pass
