# References:
# - https://mathworld.wolfram.com/LabeledTree.html


def count_possible_formula_with_exactly_n_symbols(n):
    return n ** (n - 2)


for i in range(1, 8 + 1):
    print(f'possible formula with {i} symbols: {count_possible_formula_with_exactly_n_symbols(n=i)}')

print()


def count_possible_formula_with_max_n_symbols(n):
    x = 0
    for i in range(1, n + 1):
        x = x + count_possible_formula_with_exactly_n_symbols(n=i)
    return x


for i in range(1, 8 + 1):
    print(f'possible formula with max {i} symbols: {count_possible_formula_with_max_n_symbols(n=i)}')

print()


def count_possible_formula_sequences_with_max_n_formula(max_formula, max_symbol_per_formula):
    possible_axioms = count_possible_formula_with_max_n_symbols(n=max_symbol_per_formula)
    l = 0
    for axioms in range(1, max_formula + 1):
        l = l + possible_axioms ** axioms
    return l


for i in range(1, 8):
    for j in range(1, 8):
        print(
            f'possible formula sequences with max {i} formulas and max {j} symbols per sequence: {count_possible_formula_sequences_with_max_n_formula(max_formula=i, max_symbol_per_formula=j)}')
print()


def count_possible_languages(max_axioms, max_formula_per_axiom, max_symbol_per_formula):
    x = 0
    axiom_possibilities = count_possible_formula_sequences_with_max_n_formula(max_formula=max_formula_per_axiom,
                                                                              max_symbol_per_formula=max_symbol_per_formula)
    for i in range(1, max_axioms + 1):
        x = x + axiom_possibilities ** i
    return x


for i in range(1, 8 + 1):
    for j in range(1, 8 + 1):
        for k in range(1, 8 + 1):
            print(
                f'possible languages with max {i} axioms with max {j} formula per axiom and max {k} symbol per formula: {count_possible_languages(max_axioms=i, max_formula_per_axiom=j, max_symbol_per_formula=j)}')
print()
