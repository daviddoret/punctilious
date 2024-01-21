import typing
import log
import typesetting as ts
import fl1_typesetting

treatment: ts.Treatment = fl1_typesetting.treatments.symbolic_representation
flavor: ts.Flavor = ts.flavors.default
language: ts.Language = ts.languages.enus

ts.register_symbol(tag=fl1_typesetting.connective, symbol=ts.symbols.asterisk_operator, treatment=treatment,
    flavor=flavor, language=language)

log.debug(f"Module {__name__}: loaded.")
