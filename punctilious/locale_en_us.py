import core
from core import *


class LocaleEnUs(Locale):
    """TODO: Implement localization. This is just a small example to showcase how this could be implemented."""

    def __init__(self):
        super().__init__(name='EN-US')
        self._qed = None

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

    def compose_axiom_interpretation_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, True]:
        global text_dict
        # Retrieve the parameters from the statement
        a = o.parameters[0]
        a: AxiomInclusion
        p = o.parameters[1]
        p: Formula
        yield from a.axiom.compose_natural_language()
        yield SansSerifNormal(' is postulated by ')
        yield from a.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from p.compose_formula()
        yield SansSerifNormal(' is an interpretation of that axiom.')
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

    def compose_inferred_statement_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, True]:
        yield SansSerifBold('Proof')
        yield SansSerifNormal(': ')
        # Proof premises
        if o.inference_rule.compose_paragraph_proof_method is None:
            # There is no specific proof composition method
            # linked to this inference-rule,
            # make a best-effort to write a readable proof.
            for i in range(len(o.parameters)):
                parameter = o.parameters[i]
                yield from parameter.compose_formula()
                yield SansSerifNormal(' follows from ')
                yield from parameter.compose_ref()
                yield SansSerifNormal('.')
        else:
            yield from o.inference_rule.compose_paragraph_proof_method(o=o)
        # Proof conclusion
        yield SansSerifNormal(' Therefore, by the ')
        yield from o.inference_rule.compose_dashed_name()
        yield SansSerifNormal(' inference rule, it follows that ')
        yield from o.valid_proposition.compose_formula()
        yield SansSerifNormal('. ')
        yield self.qed
        return True

    def compose_inferred_statement_report(self, o: InferredStatement,
                                          output_proof: (None, bool) = None) -> \
            collections.abc.Generator[
                Composable, Composable, True]:
        output_proof = prioritize_value(output_proof, True)
        yield o.compose_title(cap=True)
        yield SansSerifNormal(': ')
        yield from o.valid_proposition.compose_formula()
        yield SansSerifNormal('.')
        if output_proof:
            yield SansSerifNormal(' ')
            yield from self.compose_inferred_statement_paragraph_proof(o=o)
        return True

    def compose_modus_ponens_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_implies_q = o.parameters[0]
        p_implies_q: FormulaStatement
        p = o.parameters[1]
        p: FormulaStatement
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('.')
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p.compose_ref_link()
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

    def compose_variable_substitution_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, True]:
        global text_dict
        # Retrieve the parameters from the statement
        parameter = o.parameters[0]
        yield from parameter.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from parameter.compose_ref_link()
        yield SansSerifNormal('.')
        yield SansSerifNormal(' Let ')
        free_variables = parameter.get_variable_ordered_set()
        mapping = zip(free_variables, o.parameters[1:])
        first_pair = True
        for k, v in mapping:
            if not first_pair:
                yield SansSerifNormal(', ')
            yield from k.compose_symbol()
            yield ' = '
            yield from v.rep_formula()
            first_pair = False
        yield SansSerifNormal('.')
        return True

    @property
    def maps_to(self) -> StyledText:
        if self._maps_to is None:
            self._maps_to = SansSerifNormal(plaintext='|-->', unicode='↦', latex_math='\\mapsto')
        return self._maps_to

    @property
    def qed(self) -> StyledText:
        if self._qed is None:
            self._qed = SansSerifNormal(plaintext='QED', unicode='∎', latex_math='\\qed')
        return self._qed


locale_en_us = LocaleEnUs()
