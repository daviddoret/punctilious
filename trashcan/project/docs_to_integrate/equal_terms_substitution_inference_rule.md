# Equal Terms Substitution

## Definition

The inference-rule: (P, (Q=R)) ⊢ P' where:

- P is a formula-statement,
- Q=R is an equality formula-statement,
- P' is a modified formula-statement P where all occurrences of Q in P are substituted with R.

## Designations

Acronym: ets

Symbol: equal-terms-substitution

Name: equal terms substitution

## Algorithm

The algorithm for formula substitution is:

- canonical-order (top-down, depth-first, left-to-right)
- replace all occurrences until end of formula is reached

## Python implementation

- EqualTermsSubstitutionDeclaration: the inference-rule declaration-class.

- EqualTermsSubstitutionInclusion: the inference-rule inclusion-class.

- TheoryElaborationSequence.connectives.equal_terms_substitution: A shortcut to access the inference-rule
  inclusion. If the inference-rule is not yet included in the current theory, it is automatically included.

- UniverseOfDiscourse.connectives.equal_terms_substitution: A shortcut to access the inference-rule
  declaration in the universe-of-discourse. If the inference-rule is not yet declared in the current
  universe-of-discourse, it is automatically declared.

## TODO

TODO: EqualTermsSubstitution: QUESTION: equal_terms_substitution: Should we forbid the presence of Q in R or R in Q?

TODO: EqualTermsSubstitution: QUESTION: equal_terms_substitution: This version of the inference-rule replaces all
occurences of Q in R. We may wish to enrich this inference-rule and make it possible to only replace a subset of
occurences of Q in R. Let's keep this aside for future improvements.

TODO: EqualTermsSubstitution: inference-rule: equal_terms_substitution: Migrate to specialized classes

