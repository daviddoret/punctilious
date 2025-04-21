import sys

# import sympy

# Large prime numbers to participate in hashing functions,
# and mitigate the probability of a hash conflicts.
# n = sympy.randprime(0, pow(2, 2048)) # ideal
# n = sympy.randprime(0, sys.maxsize) # max computer capacity
# print(n)

connector_hash_prime: int = 1076876232711380473
formula_hash_prime: int = 5729681708660247977
structure_hash_prime: int = 8518494684108058217
