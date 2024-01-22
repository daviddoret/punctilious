import typing
import log
import typesetting as ts
import fl1_typesetting as fl1_ts


def load():
    treatment: ts.Treatment = fl1_ts.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus

    ts.register_symbol(tag=fl1_ts.tags.connective, symbol=ts.symbols.asterisk_operator, treatment=treatment,
        flavor=flavor, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
