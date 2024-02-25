import math
from math import pi, log, factorial
from scipy.special import zeta
import decimal

decimal.getcontext().prec = 256 + 3
decimal.getcontext().Emax = 999999999


def compute_pi(n):
    """
    This function calculates the value of pi to 'n' number of decimal places
    Args:
    n:   precision(Decimal places)
    Returns:
    pi:   the value of pi to n-decimal places
    """

    C = 426880 * decimal.Decimal(10005).sqrt()
    K = decimal.Decimal(6)
    M = decimal.Decimal(1)
    X = decimal.Decimal(1)
    L = decimal.Decimal(13591409)
    S = L

    # For better precision, we calculate to n+3 and truncate the last two digits
    for i in range(1, n + 3):
        M = decimal.Decimal(M * ((1728 * i * i * i) - (2592 * i * i) + (1104 * i) - 120) / (i * i * i))
        L = decimal.Decimal(545140134 + L)
        X = decimal.Decimal(-262537412640768000 * X)
        S += decimal.Decimal((M * L) / X)

    pi_string = str(C / S)[:-2]  # Pi is C/S
    pi = decimal.Decimal(pi_string)
    return pi


pi = compute_pi(n=256)


# print(pi)


def zeta_approx(x, i):
    n = decimal.Decimal(0)
    for j in range(1, i + 1):
        j = decimal.Decimal(j)
        n = n + 1 / j ** x
    return n


x = decimal.Decimal(2)

z2 = decimal.Decimal(
    1.644934004348228389597374476541858522584072378420340015704836837420157712815575002682768739357302958800421849210954690327941577980931742766292900318325750475879303033967953887679118576621884683555625714734553078007802986311505892021910880914860058997242577699
)
print(f'zeta(2): {z2}')
z3 = decimal.Decimal(
    1.202056903159592332274860231820135293499361297307552613074804236121533716786995107952393628999224950668644191465416575457503720586902374589131911812847389567613353250087788080868724040465501869828277347575666649952382506917039833559606768277887374446038801874
)
print(f'zeta(3) by 16m loops: {z3}')
pi3 = pi * pi * pi
z3_best_approx = pi3 / decimal.Decimal(26)
print(f'zeta(3) = pi^3/26 {z3_best_approx}')
z4 = 1.08232323371113819151
z5 = decimal.Decimal(
    1.036927755143369926331365486453219471268293052869769155561500170174869301306631789923583872580922155743226854820236128693703374800932751777217892421582871138185132613523540966272954246805403893170253083728946065446042356053860451671660306868825918677476002744)
print(f'zeta(5) by 16m loops: {z5}')
pi5 = pi3 * pi * pi
pi5_best_approx = pi5 / decimal.Decimal(295)
print(f'zeta(5) = pi^5/295 {pi5_best_approx}')
z6 = 1.017343061984449139714517929790920527

z_numerators = {
    2: 1, 4: 1, 6: 1, 8: 1, 10: 1, 12: 691}
z_denominators = {
    2: 6, 4: 90, 6: 945, 8: 9450, 10: 93555, 12: 638512875}

print(z_denominators.values())
# print(zeta_approx(x=3, i=16000000))
# print(pi * pi / decimal.Decimal(6))

# new_approx = decimal.Decimal(0)
# last_approx = decimal.Decimal(0)
# for i in range(1, 945):
#    last_approx = new_approx
#    last_prec = abs(last_approx - z5)
#    new_approx = pi5 / decimal.Decimal(i)
#    new_prec = abs(new_approx - z5)
#    print(f'{i} : {new_prec:8} : {new_approx}')
# if not last_prec == 0 and last_prec < new_prec:
# print(i - 1)
# print(last_prec)
# break
