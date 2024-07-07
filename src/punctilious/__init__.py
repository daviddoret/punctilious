import constants_1 as c1
import util_1 as u1
import state_1 as s1
import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
import connectives_standard_library_1 as csl1
import inference_rules_1 as ir1
import propositional_logic_syntax_1 as pls1
import minimal_logic_1 as ml1

as1._connectives.follows_from.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter='follows-from')

as1._connectives.is_a.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter='is-a')
as1._connectives.land.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.conjunction)
as1._connectives.lor.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.disjunction)
as1._connectives.implies.formula_ts = as1.typesetters.infix_formula(
    connective_typesetter=pl1.symbols.implication)
as1._connectives.algorithm.formula_ts = pl1.typesetters.text(
    text='algorithm')
as1._connectives.lnot.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter=pl1.symbols.negation)
as1._connectives.natural_transformation.formula_ts = as1.typesetters.natural_transformation()
as1._connectives.tupl.formula_ts = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_curly_brace,
    separator=pl1.symbols.comma,
    close_bracket=pl1.symbols.close_curly_brace)
as1._connectives.enumeration.formula_ts = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_curly_brace,
    separator=pl1.symbols.comma,
    close_bracket=pl1.symbols.close_curly_brace)
as1._connectives.tupl.formula_ts = as1.typesetters.bracketed_list(
    open_bracket=pl1.symbols.open_parenthesis,
    separator=pl1.symbols.comma,
    close_bracket=pl1.symbols.close_parenthesis)
as1._connectives.axiom.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='axiom')
as1._connectives.inference_rule.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='inference-rule')
as1._connectives.inference_rule.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='inference-rule')
as1._connectives.theory.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='theory')
as1._connectives.axiomatization.formula_ts = as1.typesetters.classical_formula(
    connective_typesetter='axiomatization')
as1._connectives.map.formula_ts = as1.typesetters.map()
as1._connectives.follows_from.formula_ts = as1.typesetters.derivation()
