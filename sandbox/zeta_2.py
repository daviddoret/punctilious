import math
from math import pi, log, factorial
from scipy.special import zeta
import decimal
import scipy
import scipy.interpolate

decimal.getcontext().prec = 2048
decimal.getcontext().Emax = 999999999

# n	A	B
zeta_even_coefficients_a = [
    6,
    90,
    945,
    9450,
    93555,
    638512875,
    18243225,
    325641566250,
    38979295480125,
    1531329465290625,
    13447856940643125,
    201919571963756521875,
    11094481976030578125,
    564653660170076273671875,
    5660878804669082674070015625,
    62490220571022341207266406250,
    12130454581433748587292890625]

zeta_even_coefficients_b = [
    1,
    1,
    1,
    1,
    1,
    691,
    2,
    3617,
    43867,
    174611,
    155366,
    236364091,
    1315862,
    6785560294,
    6892673020804,
    7709321041217,
    151628697551]

# zeta_even_coefficients_a = [decimal.Decimal(n) for n in zeta_even_coefficients_a]
# zeta_even_coefficients_b = [decimal.Decimal(n) for n in zeta_even_coefficients_b]
zeta_even_coefficients_y = [a / b for a, b in zip(zeta_even_coefficients_a, zeta_even_coefficients_b)]
zeta_even_coefficients_x = range(1, len(zeta_even_coefficients_y) + 1)

print(len(zeta_even_coefficients_x))
print(len(zeta_even_coefficients_y))

t1 = scipy.interpolate.BarycentricInterpolator(xi=zeta_even_coefficients_x, yi=zeta_even_coefficients_y)
t1 = scipy.interpolate.PchipInterpolator(x=zeta_even_coefficients_x, y=zeta_even_coefficients_y)

l1 = scipy.interpolate.lagrange(x=zeta_even_coefficients_x, w=zeta_even_coefficients_y)
print(l1)

import matplotlib.pyplot as plt

x = [1 + x / 50 for x in range(1, 200)]
fig, ax = plt.subplots()
ax.plot(x, t1(x))

ax.set(xlabel='x', ylabel='t1(x)',
       title='test')
ax.grid()

fig.savefig("test.png")
plt.show()
