from turtle import *
from math import pow, sqrt
from os import system as sys

G = 6.674e-11                       # Gravitational Constant
scaleFactor = 6.5562e5/2            # meters/pixel
r = [6.5562e6, 0]                   # Satellite's periapsis
M = 5.972e24                        # Earth's mass
semiMajorAxis = r[0]                # a = r for circular orbit
a = [-G*M*r[0]/pow(r[0], 3), 0]
v = [0, sqrt(G*M/r[0])]             # meters/second
dt = 0.000005                       # time portions


def pixels(meters):
    """Transform meters into pixels"""
    return meters / scaleFactor


def meters(pixels):
    """Transform pixels into meters"""
    return scaleFactor * pixels


def pixels2D(meters2D):
    """Transform 2d vector of meters into pixels"""
    return [pixels(meters2D[0]), pixels(meters2D[1])]


def meters2D(pixels2D):
    """Transform 2d vector of pixels into meters"""
    return [meters(meters2D[0]), meters(meters2D[1])]


def vec2DLength(vector):
    """Get 2d vector length"""
    return sqrt(pow(vector[0], 2) + pow(vector[1], 2))


color('white', 'black')
bgcolor('black')
speed(0)
tracer(0, 0)
pu()
fd(2)
lt(90)
begin_poly()
circle(2)
end_poly()
m1 = get_poly()
planetshape = Shape("compound")
planetshape.addcomponent(m1, "gray")
register_shape("planet", planetshape)
color('blue', 'black')
pu()
home()
dot(10)
pd()
color('white', 'black')
shape('planet')
pu()

v[0] += dt * a[0]
r = [r[0] + dt * v[0], r[1] + dt * v[1]]
setpos(pixels2D(r))

pd()

period = False

# 2, because we already did first step
i = 2
while True:
    while True:
        b = a[1]
        a = [-G*M*r[0]/pow(vec2DLength(r), 3), -G*M *
             r[1]/pow(vec2DLength(r), 3)]
        v = [v[0] + i*dt*a[0], v[1] + i*dt*a[1]]
        r = [r[0] + i*dt*v[0], r[1] + i*dt*v[1]]
        setpos(pixels2D(r))

        if (i % 150) == 0:
            update()
            sys('cls')
            print('a =', round(vec2DLength(a), 6), 'm/s^2')
            print('v =', round(vec2DLength(v), 4), 'm/s')
            print('r =', round(vec2DLength(r), len(str(dt))), 'm')

        if (b > 0.0) and (a[1] <= 0.0):
            period = True
        if period and (round(v[1], 0) == 0.0):
            v[0] = -11760

        if (-window_height()/2+50) > ycor():
            exitonclick()

        i += 1
        if i == 60000:
            i -= 900
except Exception:
    pass
