import log
import typesetting as ts
import fl1_typesetting as fl1_ts
import pl1_typesetting as pl1_ts


def load():
    language: ts.Language = ts.languages.enus

    # Classical 1
    flavor: ts.Flavor = pl1_ts.flavors.classical_1

    # Symbolic Representation
    treatment: ts.Treatment = fl1_ts.treatments.symbolic_representation

    ts.register_symbol(tag=pl1_ts.tags.conditional, symbol=ts.symbols.rightwards_arrow, treatment=treatment,
        flavor=flavor, language=language)
    ts.register_symbol(tag=pl1_ts.tags.negation, symbol=ts.symbols.not_sign, treatment=treatment, flavor=flavor,
        language=language)


load()
log.debug(f"Module {__name__}: loaded.")
