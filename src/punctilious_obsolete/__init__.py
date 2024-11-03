import constants_1 as c1
import util_1 as u1
import state_1 as s1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
import connectives_standard_library_1 as csl1
import inference_rules_1 as ir1
import meta_theory_1 as mt1
import propositional_logic_syntax_1 as pls1
import minimal_logic_1 as ml1

csl1.derivation.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter='derivation')

# csl1.is_a.formula_ts = as1.typesetters.infix_formula(
#    connective_typesetter='is-a')
csl1.land.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.conjunction)
csl1.lor.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.disjunction)
csl1.implies.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.implication)
csl1.algorithm.formula_ts = pl1.typesetters.text(
    text='algorithm')
csl1.lnot.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter=pl1.symbols.negation)
csl1.theorem.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='theorem')
csl1.inference.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='inference')
csl1.natural_transformation.formula_ts = as1.typesetters.transformation_by_variable_substitution()
csl1.tupl.formula_ts = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_curly_brace,
    separator=pl1.symbols.comma,
    close_bracket=pl1.symbols.close_curly_brace)
csl1.enumeration.formula_ts = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_curly_brace,
    separator=pl1.symbols.comma,
    close_bracket=pl1.symbols.close_curly_brace)
csl1.tupl.formula_ts = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_parenthesis,
    separator=pl1.symbols.comma,
    close_bracket=pl1.symbols.close_parenthesis)
csl1.axiom.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='axiom')
csl1.inference_rule.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='inference-rule')
csl1.syntactic_rule.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='syntactic-rule')
csl1.theory_formula.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='theory')
csl1.axiomatization.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='axiomatization')
csl1.hypothesis.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='hypothesis')
csl1.map_formula.formula_ts = as1.typesetters.map()
csl1.derivation.formula_ts = as1.typesetters.derivation()
csl1.is_a_propositional_variable.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed propositional variable')
csl1.proves.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.turnstile)
csl1.extends.formula_ts = as1.typesetters.classical_formula(connective_typesetter='extends')
# TODO: Implement a rich-string typesetter in PL1
csl1.is_inconsistent.formula_ts = as1.typesetters.unary_postfix_formula(connective_typesetter='⊢ ⊥')

# Meta-theory predicates
csl1.is_well_formed_axiom.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed axiom')
csl1.is_well_formed_enumeration.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed enumeration')
csl1.is_well_formed_formula.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed formula')
csl1.is_well_formed_inference_rule.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed inference-rule')
csl1.is_well_formed_theoretical_context.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed theoretical context')
csl1.is_well_formed_proposition.formula_ts = as1.typesetters.is_a_predicate(
    conventional_class='well-formed proposition')
