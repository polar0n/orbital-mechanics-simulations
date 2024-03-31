import math
import numpy as np


def cos(α):
    """
    Function for simplifying big equations
    """
    if α == 90 or α == 270:
        return 0.0
    return math.cos(math.radians(α))


def sin(α):
    """
    Function for simplifying big equations
    """
    if α == 0 or α == 180:
        return 0.0
    return math.sin(math.radians(α))


p = 0.23
e = 0.82
i = 90
u0 = 90
Ω = 180
ω = 260
ν0 = 190
l0 = 270
μ = 1

r = np.matrix([[cos(ν0)],
               [sin(ν0)],
               [0]])

r *= p/(1+e*cos(190))

v = np.matrix([[-sin(ν0)],
               [e + cos(ν0)],
               [0]])

v *= math.sqrt(μ/p)

R11 = cos(Ω) * cos(ω) - sin(Ω) * sin(ω) * cos(i)
R12 = -cos(Ω) * sin(ω) - sin(Ω) * cos(ω) * cos(i)
R13 = sin(Ω) * sin(i)
R21 = sin(Ω) * cos(ω) + cos(Ω) * sin(ω) * cos(i)
R22 = -sin(Ω) * sin(ω) + cos(Ω) * cos(ω) * cos(i)
R23 = -cos(Ω) * sin(i)
R31 = sin(ω) * sin(i)
R32 = cos(ω) * sin(i)
R33 = cos(i)

R = np.matrix([[R11, R12, R13],
               [R21, R22, R23],
               [R31, R32, R33]])

print(R)
print(v)
print(R * v)
