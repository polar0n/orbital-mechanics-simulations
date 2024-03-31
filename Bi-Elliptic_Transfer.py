import tkinter as tk
from tkinter import font
from turtle import *
from math import pow, sqrt, cos, sin, acos, asin, degrees as deg, radians as rad
from os import system as sys

DU = 6378145                             # Distance units

G = 6.67408e-11                          # Gravitational Constant
scaleFactor = 127562*10/4                # meters/pixel
M = 5.97237e24                           # Sun's mass
μ = G*M

r1 = 1 * DU
r2 = 10 * DU
r_ = 20 * DU
vcs1 = sqrt(μ/r1)
vcs2 = sqrt(μ/r2)
E1 = -μ/(r1+r_)
E2 = -μ/(r2+r_)
vt1 = sqrt(2*μ*r_/(r1**2+r1*r_))
vt3 = sqrt(2*μ*r_/(r2**2+r2*r_))
v1t2 = sqrt(2*μ*r1/(r_**2+r1*r_))
v2t2 = sqrt(2*μ*r2/(r_**2+r2*r_))
Δv1 = vt1 - vcs1
Δv2 = v2t2 - v1t2
Δv3 = vt3 - vcs2

r = [r1, 0]                              # Earth's periapsis
v = [0, vcs1]                            # meters/second
a = [-μ*r[0]/pow(r[0], 3), 0]
dt = 0.000008                            # time portions


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


def vec2Dadd(vector1, vector2):
    """Add two 2d vectors"""
    return [vector1[0] + vector2[0], vector1[1] + vector2[1]]


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
    Dosis = font.Font(family='Dosis', size=15)
    linespace = Dosis.metrics('linespace')

    root = getcanvas()
    telemetry = root.create_text(5-window_width()/2, -window_height()/2,
                                 fill='white', font=Dosis, anchor=tk.NW)
    root.pack()

v[0] += dt * a[0]
r = [r[0] + dt * v[0], r[1] + dt * v[1]]
satt.setpos(pixels2D(r))

satt.pd()

transfer1 = [False, False]
transfer2 = False
transfer3 = False
# 2, because we already did first step
i = 2
try:
    while True:
        a = [-μ*r[0]/pow(vec2DLength(r), 3), -μ*r[1]/pow(vec2DLength(r), 3)]
        v = [v[0] + i*dt*a[0], v[1] + i*dt*a[1]]
        r = [r[0] + i*dt*v[0], r[1] + i*dt*v[1]]
        satt.setpos(pixels2D(r))

        ϕ1 = round(deg(acos(r[0]/vec2DLength(r))), 2)
        ϕ2 = round(deg(asin(r[0]/vec2DLength(r))), 2)

        if not transfer1[0]:
            if ϕ2 < 0:
                transfer1[0] = True
        if transfer1[0] and not transfer1[1]:
            if (ϕ1 < 0.1) and (ϕ2 > 89.9):
                v[1] = v[1] + Δv1
                transfer1[1] = True
        if transfer1[1] and not transfer2:
            if (ϕ1 > 179.9) and (ϕ2 < -89.9):
                v[1] = v[1] - Δv2
                transfer2 = True
        if transfer2 and not transfer3:
            if (ϕ1 < 0.1) and (ϕ2 > 89.9):
                v[1] = v[1] - Δv3
                transfer3 = True

        if (i % 150) == 0:                  # Make a screen update once in 150 cycles of i
            if telemetryFlag == 1:          # Telemetry flag is set to 'Terminal Telemetry'
                sys('cls')
                print('a =', round(vec2DLength(a), 6), 'm/s^2')
                print('v =', round(vec2DLength(v), 4), 'm/s')
                print('r =', round(vec2DLength(r), len(str(dt))), 'm')
                print('phi1 =', ϕ1)
                print('phi2 =', ϕ2)

            if telemetryFlag == 2:          # Telemetry flag is set to 'On-Screen Telemetry'
                root.itemconfigure(telemetry, text='a = ' +
                                   str(round(vec2DLength(a), 2)) + ' m/s^2\n' + 'v = ' +
                                   str(round(vec2DLength(v), 2)) + ' m/s\n' + 'r = ' +
                                   str(round(vec2DLength(r)*1e-3, 2)) + ' km\n')

            update()        # Update the canvas (drawing scene)

        i += 1

        # Fix the i value so it cannot cause lag by being
        # too big. -150 because that's the screen update rate.
        if i == 60000:
            i = i - 900
except Exception:
    pass
