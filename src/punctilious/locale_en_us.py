import punctilious.core as core
from punctilious.core import *


class LocaleEnUs(Locale):
    """TODO: Implement localization. This is just a small example to showcase how this could be implemented."""

    def __init__(self):
        super().__init__(name='EN-US')

    def compose_absorption_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p: FormulaStatement = o.parameters[0]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from o.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from the application of the ')
        yield from o.inference_rule.compose_symbol()
        yield SansSerifNormal(' inference-rule: ')
        yield o.inference_rule.definition
        yield SansSerifNormal('.')
        return True

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
        yield from o.u.compose_symbol()
        yield from o.nameset.compose_name(pre=SansSerifNormal(', known as '))
        yield from o.nameset.compose_acronym(pre=SansSerifNormal(', or simply '))
        yield SansSerifNormal('.')
        return True

    def compose_axiom_inclusion_report(self, o: AxiomInclusion, proof: (None, bool) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
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
            collections.abc.Generator[Composable, Composable, bool]:
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
        yield SansSerifNormal(' is a propositional formula interpreted from that axiom.')
        return True

    def compose_biconditional_elimination_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        p0 = o.inference_rule.definition.parameters[0]
        p_iff_q: FormulaStatement = o.parameters[0]
        yield from p_iff_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield p0.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_iff_q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_biconditional_elimination_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        p0 = o.inference_rule.definition.parameters[0]
        q_iff_p: FormulaStatement = o.parameters[0]
        yield from q_iff_p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from p0.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from q_iff_p.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_biconditional_introduction_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p_implies_q: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p_implies_q: FormulaStatement = o.parameters[0]
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_implies_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_q_implies_p: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        q_implies_p: FormulaStatement = o.parameters[1]
        yield from q_implies_p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_q_implies_p.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from q_implies_p.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_conjunction_elimination_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        p0 = o.inference_rule.definition.parameters[0]
        p_and_q: FormulaStatement = o.parameters[0]
        yield from p_and_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield p0.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_and_q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_conjunction_elimination_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        p_and_q: FormulaStatement = o.parameters[0]
        p0 = o.inference_rule.definition.parameters[0]
        yield from p_and_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield p0.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_and_q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_conjunction_introduction_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p: FormulaStatement = o.parameters[0]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_q: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        q: FormulaStatement = o.parameters[1]
        yield from q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_constant_declaration(self, o: ConstantDeclaration) -> collections.abc.Generator[
        Composable, Composable, bool]:
        yield SansSerifNormal('Let ')
        yield from o.compose_symbol()
        yield SansSerifNormal(' be the constant ')
        yield from o.value.compose_formula()
        yield SansSerifNormal('. ')
        return True

    def compose_constructive_dilemma_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p_implies_q: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p_implies_q: FormulaStatement = o.parameters[0]
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_implies_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_r_implies_s: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        r_implies_s: FormulaStatement = o.parameters[1]
        yield from r_implies_s.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_r_implies_s.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from r_implies_s.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_p_or_r: Formula = o.inference_rule.definition.parameters[0].parameters[2]
        p_or_r: FormulaStatement = o.parameters[2]
        yield from p_or_r.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_or_r.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_or_r.compose_ref_link()
        yield SansSerifNormal('. ')
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
        yield from o.u.compose_symbol()
        yield from o.nameset.compose_name(pre=SansSerifNormal(', known as '))
        yield from o.nameset.compose_acronym(pre=SansSerifNormal(', or simply '))
        yield SansSerifNormal('.')
        return True

    def compose_definition_inclusion_report(self, o: DefinitionInclusion,
            proof: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield from o.compose_title(cap=True)
        yield SansSerifNormal(': Let ')
        yield SerifItalic('definition')
        yield SansSerifNormal(' ')
        yield from o.d.compose_symbol()
        yield SansSerifNormal(' ')
        yield text_dict.open_quasi_quote
        yield o.d.natural_language
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be included (postulated) in ')
        yield from o.theory.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_definition_interpretation_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        a: DefinitionInclusion
        p: Formula
        a = o.parameters[0]
        p = o.parameters[1]
        yield from a.d.compose_natural_language()
        yield SansSerifNormal(' is postulated by ')
        yield from a.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from p.compose_formula()
        yield SansSerifNormal(' is an interpretation of that definition.')
        return True

    def compose_destructive_dilemma_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p_implies_q: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p_implies_q: FormulaStatement = o.parameters[0]
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_implies_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_r_implies_s: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        r_implies_s: FormulaStatement = o.parameters[1]
        yield from r_implies_s.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_r_implies_s.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from r_implies_s.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_not_q_or_not_s: Formula = o.inference_rule.definition.parameters[0].parameters[2]
        not_q_or_not_s: FormulaStatement = o.parameters[2]
        yield from not_q_or_not_s.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_not_q_or_not_s.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from not_q_or_not_s.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_disjunction_introduction_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p: Formula = o.inference_rule.definition.parameters[0]
        p: FormulaStatement = o.parameters[0]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_q: Formula = o.inference_rule.definition.parameters[1].parameters[0]
        q: FormulaStatement = o.parameters[1]
        yield from q.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_q.compose_formula()
        yield SansSerifNormal(', is given. ')
        return True

    def compose_disjunction_introduction_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p: Formula = o.inference_rule.definition.parameters[0]
        p: FormulaStatement = o.parameters[0]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_q: Formula = o.inference_rule.definition.parameters[1].parameters[1]
        q: FormulaStatement = o.parameters[1]
        yield from q.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_q.compose_formula()
        yield SansSerifNormal(', is given. ')
        return True

    def compose_disjunctive_resolution_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p_or_q: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p_or_q: FormulaStatement = o.parameters[0]
        yield from p_or_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_or_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_or_q.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_not_p_or_r: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        not_p_or_r: FormulaStatement = o.parameters[1]
        yield from not_p_or_r.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_not_p_or_r.compose_formula()
        yield SansSerifNormal(', is given. ')
        return True

    def compose_disjunctive_syllogism_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p_or_q: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p_or_q: FormulaStatement = o.parameters[0]
        yield from p_or_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_or_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_or_q.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_not_p: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        not_p: FormulaStatement = o.parameters[1]
        yield from not_p.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_not_p.compose_formula()
        yield SansSerifNormal(', is given. ')
        return True

    def compose_disjunctive_syllogism_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p_or_q: Formula = o.inference_rule.definition.parameters[0].parameters[0]
        p_or_q: FormulaStatement = o.parameters[0]
        yield from p_or_q.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p_or_q.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p_or_q.compose_ref_link()
        yield SansSerifNormal('. ')
        parameter_not_q: Formula = o.inference_rule.definition.parameters[0].parameters[1]
        not_q: FormulaStatement = o.parameters[1]
        yield from not_q.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_not_q.compose_formula()
        yield SansSerifNormal(', is given. ')
        return True

    def compose_double_negation_elimination_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_not_not_p: Formula = o.inference_rule.definition.parameters[0]
        not_not_p: FormulaStatement = o.parameters[0]
        yield from not_not_p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_not_not_p.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from not_not_p.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_double_negation_introduction_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        parameter_p: Formula = o.inference_rule.definition.parameters[0]
        p: FormulaStatement = o.parameters[0]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(', of the form ')
        yield from parameter_p.compose_formula()
        yield SansSerifNormal(', follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_equality_commutativity_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_eq_q: FormulaStatement
        p_eq_q = o.parameters[0]
        yield from p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_equal_terms_substitution_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p: FormulaStatement = o.parameters[0]
        p_eq_q: FormulaStatement = o.parameters[1]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_hypothetical_syllogism_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_implies_q: FormulaStatement = o.parameters[0]
        q_implies_r: FormulaStatement = o.parameters[1]
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('. ')
        yield from q_implies_r.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from q_implies_r.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_inconsistency_introduction_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p0 = StyledText(plaintext='P', unicode='𝑷')
        p1 = StyledText(plaintext='not(P)', unicode='¬(𝑷)')
        p: FormulaStatement = o.parameters[0]
        not_p: FormulaStatement = o.parameters[1]
        yield SansSerifNormal('Let ')
        yield p0
        yield SerifItalic(' := ')
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(', which follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('. ')
        yield SansSerifNormal('Let ')
        yield p1
        yield SerifItalic(' := ')
        yield from not_p.valid_proposition.compose_formula()
        yield SansSerifNormal(', which follows from ')
        yield from not_p.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_inconsistency_introduction_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p0: StyledText = StyledText(plaintext='(P = Q)', unicode='(𝑷 = 𝑸)')
        p1: StyledText = StyledText(plaintext='(P neq Q))', unicode='(𝑷 ≠ 𝑸)')
        p_eq_q: FormulaStatement = o.parameters[0]
        p_neq_q: FormulaStatement = o.parameters[1]
        yield SansSerifNormal('Let ')
        yield p0
        yield SerifItalic(' := ')
        yield from p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal('. ')
        yield SansSerifNormal('Let ')
        yield p1
        yield SerifItalic(' := ')
        yield from p_neq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_neq_q.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_inconsistency_introduction_3_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p0: StyledText = StyledText(plaintext='(P neq P)', unicode='(𝑷 ≠ 𝑷)')
        p_neq_p: FormulaStatement = o.parameters[0]
        yield SansSerifNormal('Let ')
        yield p0
        yield SerifItalic(' := ')
        yield from p_neq_p.valid_proposition.compose_formula()
        yield SansSerifNormal(', which follows from ')
        yield from p_neq_p.compose_ref_link()
        yield SansSerifNormal('. ')
        return True

    def compose_inference_rule_declaration(self, i: InferenceRuleDeclaration) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from i.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be an ')
        yield SerifItalic('inference-rule')
        yield SansSerifNormal(' defined as ')
        if i.definition is None:
            yield '(missing definition)'
        else:
            yield text_dict.open_quasi_quote
            yield i.definition
            yield text_dict.close_quasi_quote
        yield SansSerifNormal(' in ')
        yield from i.u.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_inference_rule_inclusion_report(self, i: InferenceRuleInclusion,
            proof: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield from i.inference_rule.compose_title(cap=True)
        yield SansSerifNormal(': Let ')
        yield SerifItalic('inference-rule')
        yield SansSerifNormal(' ')
        yield from i.inference_rule.compose_symbol()
        yield SansSerifNormal(' defined as ')
        if i.inference_rule.definition is None:
            yield '(missing definition)'
        else:
            yield text_dict.open_quasi_quote
            yield i.inference_rule.definition
            yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be included and considered valid in ')
        yield from i.theory.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_inferred_statement_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        """Generic paragraph proof composition for inferred-statements.
        This method makes a best effort at composing a paragraph proof,
        but should rather be overridden by the inference-rule specialized class."""
        for i in range(len(o.parameters)):
            parameter = o.parameters[i]
            if isinstance(parameter, FormulaStatement):
                parameter: FormulaStatement
                yield from parameter.valid_proposition.compose_formula()
            else:
                yield from parameter.compose_formula()
            yield SansSerifNormal(' follows from ')
            yield from parameter.compose_ref_link()
            yield SansSerifNormal('. ')
        return True

    def compose_inferred_statement_report(self, o: InferredStatement, proof: (None, bool) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        proof = prioritize_value(proof, True)
        yield o.compose_title(cap=True)
        yield SansSerifNormal(': ')
        yield from o.valid_proposition.compose_formula()
        yield SansSerifNormal('.')
        if proof:
            yield SansSerifNormal(' ')
            yield SansSerifBold('Proof')
            yield SansSerifNormal(': ')
            yield from o.inference_rule.compose_paragraph_proof(o=o)
            # Proof conclusion
            yield SansSerifNormal(' Therefore, by the ')
            yield from o.inference_rule.inference_rule.compose_dashed_name()
            yield SansSerifNormal(' inference rule: ')
            yield o.inference_rule.definition
            yield SansSerifNormal(', it follows that ')
            yield from o.valid_proposition.compose_formula()
            yield SansSerifNormal('. ')
            yield self.qed
        return True

    def compose_modus_ponens_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_implies_q: FormulaStatement = o.parameters[0]
        p: FormulaStatement = o.parameters[1]
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('.')
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_modus_tollens_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_implies_q: FormulaStatement = o.parameters[0]
        not_q: FormulaStatement = o.parameters[1]
        yield from p_implies_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p_implies_q.compose_ref_link()
        yield SansSerifNormal('.')
        yield from not_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from not_q.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_note_report(self, o: InferredStatement, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        yield o.compose_title(cap=True)
        yield SansSerifNormal(': ')
        yield from o.compose_content()
        return True

    def compose_parent_hypothesis_statement_report(self, o: Hypothesis,
            proof: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        proof = prioritize_value(proof, True)
        yield o.compose_title(cap=True)
        yield SansSerifNormal(': ')
        yield from o.hypothesis_formula.compose_formula()
        yield SansSerifNormal('.')
        if proof:
            yield SansSerifNormal(' This hypothesis is elaborated in theory ')
            yield from o.hypothesis_child_theory.compose_symbol()
            yield SansSerifNormal('.')
        return True

    def compose_proof_by_contradiction_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_eq_q: Hypothesis = o.parameters[0]
        yield SansSerifNormal('Let ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal(' be the hypothesis ')
        yield from p_eq_q.hypothesis_formula.compose_formula()
        yield SansSerifNormal('. ')
        inc_p_eq_q: FormulaStatement = o.parameters[1]
        yield from inc_p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from inc_p_eq_q.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_proof_by_contradiction_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_eq_q: Hypothesis = o.parameters[0]
        yield SansSerifNormal('Let ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal(' be the hypothesis ')
        yield from p_eq_q.hypothesis_formula.compose_formula()
        yield SansSerifNormal('. ')
        inc_p_eq_q: FormulaStatement = o.parameters[1]
        yield from inc_p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from inc_p_eq_q.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_proof_by_refutation_1_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_eq_q: Hypothesis = o.parameters[0]
        yield SansSerifNormal('Let ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal(' be the hypothesis ')
        yield from p_eq_q.hypothesis_formula.compose_formula()
        yield SansSerifNormal('. ')
        inc_p_eq_q: FormulaStatement = o.parameters[1]
        yield from inc_p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from inc_p_eq_q.compose_ref_link()
        yield SansSerifNormal('.')
        return True

    def compose_proof_by_refutation_2_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p_eq_q: Hypothesis = o.parameters[0]
        yield SansSerifNormal('Let ')
        yield from p_eq_q.compose_ref_link()
        yield SansSerifNormal(' be the hypothesis ')
        yield from p_eq_q.hypothesis_formula.compose_formula()
        yield SansSerifNormal('. ')
        inc_p_eq_q: FormulaStatement = o.parameters[1]
        yield from inc_p_eq_q.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from inc_p_eq_q.compose_ref_link()
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
        yield from o.u.compose_symbol()
        yield SansSerifNormal('.')
        return True

    def compose_theory_declaration(self, t: TheoryDerivation) -> collections.abc.Generator[
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

    def compose_theory_article(self, t: TheoryDerivation, proof: (None, bool) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:

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
        for o in t.u.simple_objcts.values():
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
        yield from t.u.compose_symbol()
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
            yield from t.u.compose_symbol()
            yield SansSerifNormal('.')
            yield self.paragraph_end

        yield Header(plaintext='Inference rules', level=1)
        yield self.paragraph_start
        yield SansSerifNormal(
            'The following inference rules are considered valid under this theory:')
        yield self.paragraph_end
        for inference_rule in sorted(t.i.values(),
                key=lambda i: i.inference_rule.rep_dashed_name(encoding=encodings.plaintext)):
            inference_rule: InferenceRuleInclusion
            yield self.paragraph_start
            yield from inference_rule.inference_rule.compose_report()
            yield self.paragraph_end

        yield Header(plaintext='Theory elaboration sequence', level=1)
        for s in t.statements:
            s: Statement
            yield self.paragraph_start
            yield from s.compose_report(proof=proof)
            yield self.paragraph_end
        return True

    def compose_variable_substitution_paragraph_proof(self, o: InferredStatement) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        # Retrieve the parameters from the statement
        p = o.parameters[0]
        yield from p.valid_proposition.compose_formula()
        yield SansSerifNormal(' follows from ')
        yield from p.compose_ref_link()
        yield SansSerifNormal('.')
        yield SansSerifNormal(' Let ')
        variables = p.get_unique_variable_ordered_set
        parameter_o: Formula = o.parameters[1]
        mapping = zip(variables, parameter_o.parameters)
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
            self._maps_to = SansSerifNormal(plaintext='|-->', unicode='↦', latex='\\mapsto')
        return self._maps_to

    @property
    def paragraph_end(self) -> StyledText:
        if self._paragraph_end is None:
            self._paragraph_end = SansSerifNormal(plaintext='\n', unicode='\n', latex='')
        return self._paragraph_end

    @property
    def paragraph_start(self) -> StyledText:
        if self._paragraph_start is None:
            self._paragraph_start = SansSerifNormal(plaintext='', unicode='', latex='')
        return self._paragraph_start

    @property
    def qed(self) -> StyledText:
        if self._qed is None:
            self._qed = SansSerifNormal(plaintext='QED', unicode='∎', latex='\\qed')
        return self._qed


locale_en_us = LocaleEnUs()
