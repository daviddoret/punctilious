from core import *


class LocaleEnUs(Locale):
    """TODO: Implement localization. This is just a small example to showcase how this could be implemented."""

    def __init__(self):
        super().__init__(name='EN-US')

    def compose_axiom_declaration(self, o: AxiomDeclaration) -> collections.abc.Generator[
        Composable, Composable, True]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from o.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be the ')
        yield SerifItalic('axiom')
        yield SansSerifNormal(' ')
        yield text_dict.open_quasi_quote
        yield o.natural_language
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' in ')
        yield from o.universe_of_discourse.compose_symbol()
        yield from o.nameset.compose_name(pre=SansSerifNormal(', known as '))
        yield from o.nameset.compose_acronym(pre=SansSerifNormal(', or simply '))
        yield SansSerifNormal('.')
        return True

    def compose_axiom_inclusion_report(self, o: AxiomInclusion) -> collections.abc.Generator[
        Composable, Composable, True]:
        global text_dict
        yield from o.compose_title(cap=True)
        yield SansSerifNormal(': Let ')
        yield SerifItalic('axiom')
        yield SansSerifNormal(' ')
        yield from o.axiom.compose_symbol()
        yield SansSerifNormal(' ')
        yield text_dict.open_quasi_quote
        yield o.axiom.natural_language
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be included (postulated) in ')
        yield from o.theory.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_definition_declaration(self, o: DefinitionDeclaration) -> collections.abc.Generator[
        Composable, Composable, True]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from o.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be the ')
        yield SerifItalic('definition')
        yield SansSerifNormal(' ')
        yield text_dict.open_quasi_quote
        yield o.natural_language
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' in ')
        yield from o.universe_of_discourse.compose_symbol()
        yield from o.nameset.compose_name(pre=SansSerifNormal(', known as '))
        yield from o.nameset.compose_acronym(pre=SansSerifNormal(', or simply '))
        yield SansSerifNormal('.')
        return True

    def compose_definition_inclusion_report(self, o: DefinitionInclusion) -> \
            collections.abc.Generator[
                Composable, Composable, True]:
        global text_dict
        yield from o.compose_title()
        yield SansSerifNormal(': Let ')
        yield SerifItalic('definition')
        yield SansSerifNormal(' ')
        yield from o.definition.compose_symbol()
        yield SansSerifNormal(' ')
        yield text_dict.open_quasi_quote
        yield o.definition.natural_language
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be included (postulated) in ')
        yield from o.theory.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_simple_objct_declaration(self, o: SimpleObjct) -> collections.abc.Generator[
        Composable, Composable, True]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from o.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be a ')
        yield SerifItalic('simple-object')
        yield SansSerifNormal(' in ')
        yield from o.universe_of_discourse.compose_symbol()
        yield SansSerifNormal('.')
        return True


locale_en_us = LocaleEnUs()
