# stabilized (of theory elaboration)

## Definition

In _punctilious_, a _theory elaboration_ 𝑡 is _stabilized_ when:

- we forbid the introduction of new _inference rules_ in 𝑡,
- we forbid the postulation of new _contentual_ _axioms_ in 𝑡,
- we forbid the direct inference of new _propositions_ from 𝑡's _contentual_ axioms.

## Use case

In the process of elaborating theories, the author should expressly mark the theory as _stabilized_ once all inference
rules, axioms, and direct axiom inferences have been made. From that point onward, the fundamental properties of the
theory won't change anymore and further theory elaboration will only reveal the underlying theory.

In _punctilious_, to stabilize a theory elaboration, use the following method:

```python
# Assuming t is an instance of TheoryElaboration.
t.stabilize()
```

Note that it is still possible to elaborate free-extensions of 𝑡, and to allow new inference rules, postulate new
axioms, and make new direct axiom inferences in theory extensions of t. Conversely, stable-extensions of 𝑡 are
stabilized by definition.

## Rationale

The introduction of new _inference rules_ in 𝑡 could allow the inference of statements that would be impossible
otherwise. This is the case if the newly allowed _inference rule_ is unsound and allows the
inference of contradictory statements. This is more generally the case if the newly allowed _inference rule_ cannot be
derived from the existing inference rules.

The introduction of new _contentual_ _axioms_ in 𝑡 could allow the inference of statements otherwise impossible, or
limit the statements that would are possible.

The direct inference of new propositions from axioms could bring

Conversely, the introduction of new _definitions_ and _direct-definition-inferences_ do not modify the stability of the 




