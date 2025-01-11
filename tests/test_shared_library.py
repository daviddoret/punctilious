import pytest
import punctilious as pu


def create_atomic_connector(c: str):
    ren = pu.rpr.RendererForStringConstant(string_constant=c)
    rep = pu.rpr.AbstractRepresentation(uid=pu.ids.create_uid(f'rep'), renderers=(ren,))
    con = pu.fml.Connector(uid=pu.ids.create_uid(f'con'), connector_representation=rep,
                           formula_representation=pu.formula_notations.atomic_formula)
    return con


def create_function(c: str):
    string_template = ('{{ connector }}'
                       '({% for argument in arguments %}{{ argument }}{% if not loop.last %}, {% endif %}'
                       '{% endfor %})')
    ren = pu.rpr.RendererForStringTemplate(string_template=string_template)
    rep = pu.rpr.AbstractRepresentation(uid=pu.ids.create_uid(f'rep'), renderers=(ren,))
    con = pu.Connector(uid=pu.ids.create_uid(f'fun'), connector_representation=rep,
                       formula_representation=pu.formula_notations.function_formula)
    return con
