# variable-substitution

## Definition

_variable substitution_

...produces a _substition instance_ of the original formula.

## See also

* Substitution (for formulae in general)

## Bibliography

* Crabbe, 2004
* nLab, 2023
* Wikipedia, Substitution (Logic), URL:

        """An inference-rule: P, X→Y ⊢ P' where:
         - P is an input statement,
         - X→Y is a mapping between the variables in P and their substitution values,
         - P' is a new formula identical to P except that variables have been
           substituted according to the X→Y mapping.

        In practice, the mapping X→Y is implicit. A sequence Y' of substitution values
        is provided as an input, where substitution values are indexed by the canonical-order
        of their corresponding variables in the ordered set of variables in P.

        Abridged property: u.i.vs

        Formal definition:
        Given a statement P whose formula contains an ordered set
        of n variables, ordered by their canonical order of
        appearance in the formula,
        given an ordered set of theoretical-objcts O of cardinality n,
        the _variable substitution_ _inference rule_ returns a new
        statement P' where all occurrences of variables in P were
        replaced by their corresponding substitution values in O.

        Warning:
        To avoid inconsistent package, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

An inference-rule: P, X→Y ⊢ P' where:

- P is an input statement,
- X→Y is a mapping between the variables in P and their substitution values,
- P' is a new formula identical to P except that variables have been
  substituted according to the X→Y mapping.

        In practice, the mapping X→Y is implicit. A sequence Y' of substitution values
        is provided as an input, where substitution values are indexed by the canonical-order
        of their corresponding variables in the ordered set of variables in P.

        Abridged property: u.i.vs

        Formal definition:
        Given a statement P whose formula contains an ordered set
        of n variables, ordered by their canonical order of
        appearance in the formula,
        given an ordered set of theoretical-objcts O of cardinality n,
        the _variable substitution_ _inference rule_ returns a new
        statement P' where all occurrences of variables in P were
        replaced by their corresponding substitution values in O.

        Warning:
        To avoid inconsistent package, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.