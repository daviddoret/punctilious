import punctilious as pu
import random

ALPHABET_SIZE = 4
MAX_SEQUENCE_SIZE = 20

for sequence_size in range(1, MAX_SEQUENCE_SIZE):
    s = (random.randint(0, ALPHABET_SIZE) for e in range(sequence_size))
    s = pu.nn0sl.NaturalNumber0Sequence(*s)
    r1 = pu.nn0sl.AdjustedSumFirstLengthSecondReverseLexicographicThirdOrder.rank(s)
    r2 = pu.nn0sl.RefinedGodelNumberOrder.rank(s)
    print(f"{s}")
    print(f"    {r1}")
    print(f"    {r2}")
    if r1 < r2:
        print("lex < GODEL")
    if r1 > r2:
        print("LEX > godel")
    if r1 == r2:
        print("lex == godel")
