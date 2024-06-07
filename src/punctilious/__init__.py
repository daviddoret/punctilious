import util_1
import state_1
import presentation_layer_1
import axiomatic_system_1
import inference_rules_1
import propositional_logic_syntax_1
import minimal_logic_1

u1 = util_1
st1 = state_1
pl1 = presentation_layer_1
as1 = axiomatic_system_1
ir1 = inference_rules_1
pls1 = propositional_logic_syntax_1
ml1 = minimal_logic_1

as1.connectives.follows_from.formula_typesetter = as1.typesetters.infix_formula(
    connective_typesetter='follows-from')

as1.connectives.is_a.formula_typesetter = as1.typesetters.infix_formula(
    connective_typesetter='is-a')
as1.connectives.land.formula_typesetter = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.conjunction)
as1.connectives.lor.formula_typesetter = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.disjunction)
as1.connectives.implies.formula_typesetter = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.implication)
as1.connectives.lnot.formula_typesetter = as1.typesetters.classical_formula(
    connective_typesetter=pl1.symbols.negation)
as1.connectives.transformation.formula_typesetter = as1.typesetters.transformation()
as1.connectives.tupl.formula_typesetter = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_curly_brace,
    separator=pl1.symbols.collection_separator,
    close_bracket=pl1.symbols.close_curly_brace)
as1.connectives.enumeration.formula_typesetter = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_curly_brace,
    separator=pl1.symbols.collection_separator,
    close_bracket=pl1.symbols.close_curly_brace)
as1.connectives.tupl.formula_typesetter = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_parenthesis,
    separator=pl1.symbols.collection_separator,
    close_bracket=pl1.symbols.close_parenthesis)
as1.connectives.axiom.formula_typesetter = as1.typesetters.classical_formula(
    connective_typesetter='axiom')
as1.connectives.inference_rule.formula_typesetter = as1.typesetters.classical_formula(
    connective_typesetter='inference-rule')
as1.connectives.theory.formula_typesetter = as1.typesetters.classical_formula(
    connective_typesetter='theory')
as1.connectives.axiomatization.formula_typesetter = as1.typesetters.classical_formula(
    connective_typesetter='axiomatization')
as1.connectives.map.formula_typesetter = as1.typesetters.classical_formula(
    connective_typesetter='map')
