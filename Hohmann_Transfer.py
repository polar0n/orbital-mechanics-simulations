from turtle import *
from math import pow, sqrt, acos, asin, degrees
from os import system as sys
import tkinter as tk
from tkinter import font

G = 6.67408e-11                          # Gravitational Constant
scaleFactor = 30000/7                    # meters/pixel
M = 5.97237e24                           # Sun's mass
μ = G*M

r1 = 185000
r2 = 1100000
vcs1 = sqrt(μ/r1)
vcs2 = sqrt(μ/r2)
Et = - μ/(r1 + r2)
v1 = sqrt(2 * (μ/r1 + Et))
v2 = sqrt(2 * (μ/r2 + Et))
Δv1 = v1 - vcs1
Δv2 = vcs2 - v2

r = [0, -r1]                              # Earth's periapsis
v = [vcs1, 0]                             # meters/second
a = [-μ*r[1]/pow(r[1], 3), 0]
dt = 0.00000008                           # time portions


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


satt = Turtle()

satt.color('white', 'black')
bgcolor('black')
satt.speed(0)
tracer(0, 0)
satt.color('blue', 'black')
satt.dot(10)
satt.color('white', 'black')
satt.pu()
satt.fd(3)
satt.lt(90)
satt.begin_poly()
satt.circle(3, 360)
satt.end_poly()
m1 = satt.get_poly()
planetshape = Shape("compound")
planetshape.addcomponent(m1, "gray")
register_shape("planet", planetshape)
satt.shape('planet')
satt.pu()

telemetryFlag = numinput('Telemetry',
                         'No telemetry: 0\nConsole telemetry: 1\nOnscreen telemetry: 2',
                         0, minval=0, maxval=2)

# If user chose On-Screen(canvas/drawing scene) telemetry
if telemetryFlag == 2:
    Dosis = font.Font(family='Dosis', size=20)
    linespace = Dosis.metrics('linespace')

    root = getcanvas()
    telemetry = root.create_text(5-window_width()/2, -window_height()/2,
                                 fill='white', font=Dosis, anchor=tk.NW)
    root.pack()

v[0] += dt * a[0]
r = [r[0] + dt * v[0], r[1] + dt * v[1]]
satt.setpos(pixels2D(r))

satt.pd()

preOrbit = False
transOrbit = False
injectOrbit = False
# 2, because we already did first step
i = 2
try:
    while True:
        a = [-μ*r[0]/pow(vec2DLength(r), 3), -μ*r[1]/pow(vec2DLength(r), 3)]
        v = [v[0] + i*dt*a[0], v[1] + i*dt*a[1]]
        r = [r[0] + i*dt*v[0], r[1] + i*dt*v[1]]
        satt.setpos(pixels2D(r))

        ϕ1 = round(degrees(acos(r[0]/vec2DLength(r))))
        ϕ2 = round(degrees(asin(r[1]/vec2DLength(r))))

        if not preOrbit and i > 2000:
            if (ϕ1 > 89.9) and (ϕ1 < 91.1) and (ϕ2 < -89.9) and (ϕ2 > -91.1):
                preOrbit = True

        if preOrbit and (not transOrbit):
            v[0] += Δv1
            transOrbit = True

        if not injectOrbit and transOrbit:
            if (ϕ1 > 89.9) and (ϕ1 < 91.1) and (ϕ2 > 89.9) and (ϕ2 < 91.1):
                v[0] -= Δv2
                injectOrbit = True

        if (i % 60) == 0:                  # Make a screen update once in 150 cycles of i
            if telemetryFlag == 1:          # Telemetry flag is set to 'Terminal Telemetry'
                sys('cls')
                print('a =', round(vec2DLength(a), 6), 'm/s^2')
                print('v =', round(vec2DLength(v), 4), 'm/s')
                print('r =', round(vec2DLength(r), len(str(dt))), 'm')

            if telemetryFlag == 2:          # Telemetry flag is set to 'On-Screen Telemetry'
                root.itemconfigure(telemetry, text='a = ' +
                                   str(round(vec2DLength(a), 2)) + ' m/s^2\n' + 'v = ' +
                                   str(round(vec2DLength(v), 2)) + ' m/s\n' + 'r = ' +
                                   str(round(vec2DLength(r)*1e-3, 2)) + ' km\n')

            update()        # Update the canvas (drawing scene)

        i += 1

        # Fix the i value so it cannot cause lag by being
        # too big. -60 because that's the screen update rate.
        if i == 60000:
            i = i - 600
except Exception:
    pass
