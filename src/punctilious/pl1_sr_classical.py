import log
import typesetting as ts
import fl1_typesetting as fl_typesetting
import pl1_typesetting

language: ts.Language = ts.languages.enus

# Classical 1
flavor: ts.Flavor = pl1_typesetting.flavors.classical_1

# Symbolic Representation
treatment: ts.Treatment = fl_typesetting.treatments.symbolic_representation

ts.register_symbol(tag=pl1_typesetting.connective_negation, symbol=ts.symbols.not_sign, treatment=treatment,
    flavor=flavor, language=language)
ts.register_symbol(tag=pl1_typesetting.connective_material_implication, symbol=ts.symbols.rightwards_arrow,
    treatment=treatment, flavor=flavor, language=language)

log.debug(f"Module {__name__}: loaded.")
