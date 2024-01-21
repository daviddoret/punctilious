import log
import typesetting as ts
import fl1_typesetting as fl_typesetting
import pl1_typesetting


def load():
    language: ts.Language = ts.languages.enus

    # Classical 1
    flavor: ts.Flavor = pl1_typesetting.flavors.classical_1

    # Symbolic Representation
    treatment: ts.Treatment = fl_typesetting.treatments.symbolic_representation

    ts.register_symbol(tag="pl1.connective.negation", symbol=ts.symbols.not_sign, treatment=treatment, flavor=flavor,
        language=language)
    ts.register_symbol(tag="pl1.connective.material_implication", symbol=ts.symbols.rightwards_arrow,
        treatment=treatment, flavor=flavor, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
