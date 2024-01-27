import log
import typesetting as ts
import fl1
import pl1


def load():
    # Representation: Common Language
    # Flavor: Default
    # Language: EN-US
    treatment: ts.Treatment = fl1.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus
    ts.register_styledstring(tag=pl1.tags.conditional, text="material implication", treatment=treatment, flavor=flavor,
        language=language)
    ts.register_styledstring(tag=pl1.tags.negation, text="negation", treatment=treatment, flavor=flavor,
        language=language)

    # Representation: Common Language
    # Flavor: Default
    # Language: FR-CH
    treatment: ts.Treatment = fl1.treatments.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.frch
    ts.register_styledstring(tag=pl1.tags.conditional, text="conditionnel", treatment=treatment, flavor=flavor,
        language=language)
    ts.register_styledstring(tag=pl1.tags.negation, text="négation", treatment=treatment, flavor=flavor,
        language=language)

    # Representation: Symbolic Representation
    # Flavor: Default
    # Language: EN-US
    treatment: ts.Treatment = fl1.treatments.symbolic_representation
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.enus
    ts.register_symbol(tag=pl1.tags.conditional, symbol=ts.symbols.rightwards_arrow, treatment=treatment, flavor=flavor,
        language=language)
    ts.register_symbol(tag=pl1.tags.negation, symbol=ts.symbols.not_sign, treatment=treatment,
        flavor=pl1.flavors.connective_negation_not, language=language)
    ts.register_symbol(tag=pl1.tags.negation, symbol=ts.symbols.tilde, treatment=treatment,
        flavor=pl1.flavors.connective_negation_tilde, language=language)


load()
log.debug(f"Module {__name__}: loaded.")
