import typing

import fl1_typesetting
import log
import typesetting as ts
import fl1_typesetting as fl_tags


def load():
    treatment: ts.Treatment = fl1_typesetting.treatments.common_language
    flavor: ts.Flavor = ts.flavors.default
    language: ts.Language = ts.languages.frch

    ts.register_styledstring(tag=fl_tags.connective, text="connecteur", treatment=treatment, flavor=flavor,
        language=language)


load()
log.debug(f"Module {__name__}: loaded.")
