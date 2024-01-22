import typing

import log
import typesetting as ts
import fl1_typesetting as fl1_ts


def load():
    treatment: ts.Treatment = fl1_ts.treatments.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.frch

    ts.register_styledstring(tag=fl1_ts.tags.connective, text="connecteur", treatment=treatment, flavor=flavor,
        language=language)


load()
log.debug(f"Module {__name__}: loaded.")
