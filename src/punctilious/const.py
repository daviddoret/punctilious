# Large prime numbers to participate in hashing functions,
# and mitigate the probability of a hash conflict.

import sys
import sympy

# n = sympy.randprime(0, pow(2, 2048))
n = sympy.randprime(0, sys.maxsize)
print(n)

connector_prime: int = 1076876232711380473
formula_prime: int = 5729681708660247977
structure_prime: int = 8518494684108058217
