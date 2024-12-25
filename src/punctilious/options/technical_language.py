import punctilious._representation as _representation

unicode_basic = _representation.Option('technical_language', 'unicode_basic')
"""The representation is made using a subset of well-supported Unicode characters.
This option should be supported in nearly all environments."""

unicode_extended = _representation.Option('technical_language', 'unicode_extended')
"""The representation is made using an extended set of mathematical Unicode characters.
Examples: `∧`, `∨`, `∀`, `∃`, `ℕ`, `𝛽`, `∈`, `𝑥`, `𝑦`, `𝑧`.
This option should be supported in most environments."""

latex_math = _representation.Option('technical_language', 'latex_math')
"""The representation is made using LaTeX math mode.
This option is only supported in environments able to render LaTeX."""

pass
