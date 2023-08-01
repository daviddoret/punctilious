import core
from core import *


class LocaleEnUs(Locale):
    """TODO: Implement localization. This is just a small example to showcase how this could be implemented."""

    def __init__(self):
        super().__init__(name='EN-US')

    def compose_axiom_declaration(self, o: AxiomDeclaration) -> collections.abc.Generator[
        Composable, Composable, bool]:
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

    def compose_axiom_inclusion_report(self, o: AxiomInclusion, proof: (None, bool) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
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
                Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        a: AxiomInclusion
        p: Formula
        a = o.parameters[0]
        p = o.parameters[1]
        yield from a.axiom.compose_natural_language()
        yield SansSerifNormal(' is postulated by ')
        yield from a.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from p.compose_formula()
        yield SansSerifNormal(' is an interpretation of that axiom.')
        return True

    def compose_definition_declaration(self, o: DefinitionDeclaration) -> collections.abc.Generator[
        Composable, Composable, bool]:
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

    def compose_definition_inclusion_report(self, o: DefinitionInclusion,
                                            proof: (None, bool) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        yield from o.compose_title(cap=True)
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

    def compose_definition_interpretation_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        a: DefinitionInclusion
        p: Formula
        a = o.parameters[0]
        p = o.parameters[1]
        yield from a.definition.compose_natural_language()
        yield SansSerifNormal(' is postulated by ')
        yield from a.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from p.compose_formula()
        yield SansSerifNormal(' is an interpretation of that definition.')
        return True

    def compose_equality_commutativity_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_equal_q: FormulaStatement
        p_equal_q = o.parameters[0]
        yield from p_equal_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_equal_q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_equal_terms_substitution_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p: FormulaStatement
        p_equal_q: FormulaStatement
        p = o.parameters[0]
        p_equal_q = o.parameters[1]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from p_equal_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_equal_q.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_inference_rule_declaration(self, i: InferenceRuleDeclaration) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from i.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be the ')
        yield SerifItalic('inference-rule')
        yield SansSerifNormal(' TODO: COMPLETE HERE')
        yield SansSerifNormal('.')
        return True

    def compose_inference_rule_inclusion_report(self, i: InferenceRuleInclusion,
                                                proof: (None, bool) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        global text_dict
        yield from i.compose_title(cap=True)
        yield SansSerifNormal(': Let ')
        yield SerifItalic('inference-rule')
        yield SansSerifNormal(' ')
        yield from i.inference_rule.compose_symbol()
        yield SansSerifNormal(' TODO: COMPLETE')
        # TODO: yield i.inference_rule.definition
        yield SansSerifNormal(' be included (considered valid) in ')
        yield from i.theory.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_inferred_statement_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
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
                                          proof: (None, bool) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        proof = prioritize_value(proof, True)
        yield o.compose_title(cap=True)
        yield SansSerifNormal(': ')
        yield from o.valid_proposition.compose_formula()
        yield SansSerifNormal('.')
        if proof:
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
        Composable, Composable, bool]:
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

    def compose_theory_declaration(self, t: TheoryElaborationSequence) -> collections.abc.Generator[
        Composable, Composable, bool]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from t.nameset.compose_qualified_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be a ')
        yield from t.compose_class()
        yield SansSerifNormal(' in ')
        yield from t.u.compose_symbol()
        yield text_dict.period
        return True

    def compose_theory_report(self, t: TheoryElaborationSequence, proof: (None, bool) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:

        yield self.paragraph_start
        yield from t.rep_name()
        yield self.paragraph_end

        yield Header(plaintext='Theory properties', level=1)
        yield self.paragraph_start
        yield SansSerifBold('Consistency: ')
        yield str(t.consistency)
        yield self.paragraph_end
        yield self.paragraph_start
        yield SansSerifBold('Stabilized: ')
        yield str(t.stabilized)
        yield self.paragraph_end
        yield self.paragraph_start
        yield SansSerifBold('Extended theory: ')
        yield 'N/A' if t.extended_theory is None else t.extended_theory.rep_fully_qualified_name()
        yield self.paragraph_end

        yield Header(plaintext='Simple-objects declarations', level=1)
        yield self.paragraph_start
        yield SansSerifNormal('Let ')
        first_item = True
        for o in t.universe_of_discourse.simple_objcts.values():
            # TODO: Filter on simple-objects that are effectively present in the theory.
            if not first_item:
                yield ', '
            yield text_dict.open_quasi_quote
            yield from o.compose_symbol()
            yield text_dict.close_quasi_quote
            first_item = False
        yield SansSerifNormal(' be ')
        yield SerifItalic('simple-objects')
        yield SansSerifNormal(' in ')
        yield from t.universe_of_discourse.compose_symbol()
        yield SansSerifNormal('.')
        yield self.paragraph_end

        yield Header(plaintext='Relations', level=1)
        # TODO: Show default notations (infix, postfix, prefix)
        arities = frozenset(r.arity for r in t.iterate_relations())
        for a in arities:
            yield self.paragraph_start
            yield SansSerifNormal('Let ')
            first_item = True
            plural = False
            for r in (r for r in t.iterate_relations() if r.arity == a):
                r: Relation
                if not first_item:
                    yield SansSerifNormal(', ')
                    plural = True
                yield text_dict.open_quasi_quote
                yield from r.compose_symbol()
                yield text_dict.close_quasi_quote
                first_item = False
            yield SansSerifNormal(' be ')
            if plural:
                yield SerifItalic(rep_arity_as_text(a))
                yield SerifItalic('-relations')
            else:
                yield SansSerifNormal('a ')
                yield SerifItalic(rep_arity_as_text(a))
                yield SerifItalic('-relation')
            yield SansSerifNormal(' in ')
            yield from t.universe_of_discourse.compose_symbol()
            yield SansSerifNormal('.')
            yield self.paragraph_end

        yield Header(plaintext='Inference rules', level=1)
        yield self.paragraph_start
        yield SansSerifNormal(
            'The following inference rules are considered valid under this theory:')
        yield self.paragraph_end
        for inference_rule in sorted(t.i.values(),
                                     key=lambda i: i.inference_rule.rep_dashed_name(
                                         encoding=encodings.plaintext)):
            inference_rule: InferenceRuleInclusion
            yield self.paragraph_start
            yield from inference_rule.inference_rule.compose_declaration()
            yield self.paragraph_end

        yield Header(plaintext='Theory elaboration sequence', level=1)
        for s in t.statements:
            s: Statement
            yield self.paragraph_start
            yield from s.compose_report(proof=proof)
            yield self.paragraph_end
        return True

    def compose_variable_substitution_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
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
    def paragraph_end(self) -> StyledText:
        if self._paragraph_end is None:
            self._paragraph_end = SansSerifNormal(plaintext='\n', unicode='\n', latex_math='')
        return self._paragraph_end

    @property
    def paragraph_start(self) -> StyledText:
        if self._paragraph_start is None:
            self._paragraph_start = SansSerifNormal(plaintext='', unicode='', latex_math='')
        return self._paragraph_start

    @property
    def qed(self) -> StyledText:
        if self._qed is None:
            self._qed = SansSerifNormal(plaintext='QED', unicode='∎', latex_math='\\qed')
        return self._qed


locale_en_us = LocaleEnUs()
