# NEXT STEPS

# TODO: UniverseOfDiscourse: Develop a declare_universe_of_discourse() method to allow the declaration of new universes-of-discourse as objects of a parent universe-of-discourse. See articles on creation and declaration for details.

# TODO: Propositional logic: Implement the tautological-equivalence operator accompanied with a solver algorithm.

# TODO: Propositional logic: Implement the tautological-consequence operator accompanied with a solver algorithm.

# TODO: Propositional logic: Implement the negative-normal-form "macro".

# TODO: Propositional logic: Implement the conjunctive-normal-form (CNF) "macro".
# Reference: https://en.wikipedia.org/wiki/Conjunctive_normal_form

# TODO: Propositional logic: Implement the disjunctive-normal-form (DNF) "macro".

# TODO: Enrich the data model with canonical-normal-form
# Reference: https://en.wikipedia.org/wiki/Canonical_normal_form

# TODO: Enrich the data model with truth-functional-completeness.
#   - For all natively supported logics, demonstrate they are truth-functional-complete.

# TODO: Connectives: add a property to distinguish "basic" or fundamental connectives of the language, from "defined"
#  connectives that are build on top of "basic" or other "defined" connectives.

# TODO: Propositional logic: implement connective property "truth-functional". If a connective is truth-functional,
#  providing its arguments are propositional logic formulae, it assures to output either True or False and may be
#  expressed in a truth-table.

# TODO: Connectives: implement "provable-properties" (commutativity, idempotence, associativity, etc.). Possible
#  values should be: "Proven true", "Proven false", "Not proven". If "Proven true" or "Proven false",
#  a "demonstration" property must be linked to the property.

# TODO: Formula: implement equivalent formula pairs, or "identities". These should be listed in a collection linked
#  to the language / theory for easy retrieval. They must be linked to demonstrations as well.
#  Examples:
#   law-of-contrapostion: P → Q is equivalent to ¬Q → ¬P.
#   etc. De Morgan's laws, etc., etc.
