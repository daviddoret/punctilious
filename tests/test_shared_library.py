import pytest
import punctilious as pu


def create_atomic_connector(c: str):
    ren = pu.RendererForStringConstant(string_constant=c)
    rep = pu.Representation(renderers=(ren,))
    con = pu.Connector(slug=c, connector_representation=rep)
    return con


def create_function(c: str):
    string_template = '{{ connector }}({% for argument in arguments %}{{ argument }}{% if not loop.last %}, {% endif %}{% endfor %})'
    ren = pu.RendererForStringTemplate(string_template=string_template)
    rep = pu.Representation(renderers=(ren,))
    con = pu.Connector(slug=c, connector_representation=rep)
    return con
