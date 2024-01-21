import typing

import fl1_typesetting
import typesetting as ts
import fl1_typesetting as fl_tags

treatment: ts.Treatment = fl1_typesetting.treatments.common_language
flavor: ts.Flavor = ts.flavors.default
language: ts.Language = ts.languages.enus

ts.register_symbol(tag=fl_tags.connective, symbol=ts.symbols.asterisk_operator,
    treatment=ts.treatments.symbolic_representation, flavor=flavor, language=language)

log.debug(f"Module {__name__}: loaded.")
