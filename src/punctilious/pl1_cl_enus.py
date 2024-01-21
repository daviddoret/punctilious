import log
import typesetting as ts
import fl1_typesetting as fl1_ts
import pl1_typesetting as pl1_ts

language: ts.Language = ts.languages.enus

# Classical 1
flavor: ts.Flavor = pl1_ts.flavors.classical_1

# Common Language Representation
treatment: ts.Treatment = fl1_ts.treatments.common_language

ts.register_styledstring(tag=pl1_ts.connective_negation, text="negation", treatment=treatment, flavor=flavor,
    language=language)
ts.register_styledstring(tag=pl1_ts.connective_material_implication, text="material implication", treatment=treatment,
    flavor=flavor, language=language)

log.debug(f"Module {__name__}: loaded.")
