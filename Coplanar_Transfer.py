import tkinter as tk
from tkinter import font
from turtle import *
from math import pow, sqrt, cos, sin, acos, asin, degrees as deg, radians as rad
from os import system as sys

G = 6.67408e-11                          # Gravitational Constant
scaleFactor = 127562                     # meters/pixel
M = 5.97237e24                           # Sun's mass
μ = G*M

r1 = 12756290
r2 = 31890725
vcs1 = 5589.93951873234
vcs2 = 3535.388172355931
Δv1 = 4128.074750670561
Δv2 = 2957.5409961934706
v1 = 7069.938525365986
ν = -4.15                    # Angle at which injection into ellipse will be done
α = -2.045                   # Angle created by Δv1
θ = 49.51                    # Angle at which inkection into circular orbit will be done
β = 180 + 24.75              # Angle created by Δv2

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

transOrbit = False
# 2, because we already did first step
i = 2
transOrbit = [False for _ in range(3)]
postOrbit = False
try:
    while True:
        a = [-μ*r[0]/pow(vec2DLength(r), 3), -μ*r[1]/pow(vec2DLength(r), 3)]
        v = [v[0] + i*dt*a[0], v[1] + i*dt*a[1]]
        r = [r[0] + i*dt*v[0], r[1] + i*dt*v[1]]
        satt.setpos(pixels2D(r))

        ϕ1 = round(deg(acos(r[0]/vec2DLength(r))), 2)
        ϕ2 = round(deg(asin(r[0]/vec2DLength(r))), 2)

        if not transOrbit[0]:
            if (ϕ1 > 90) and (ϕ2 < 0):
                transOrbit[0] = True
        if transOrbit[0] and not transOrbit[1]:
            if (ϕ1 > 4.1) and (ϕ1 < 4.2) and (ϕ2 > 85.8) and (ϕ2 < 85.9):
                transOrbit[1] = True

        if transOrbit[0] and transOrbit[1] and not transOrbit[2]:
            Δv1 = [Δv1*cos(rad(α)), Δv1*sin(rad(α))]
            v = vec2Dadd(v, Δv1)
            transOrbit[2] = True

        if transOrbit[2] and not postOrbit:
            if (ϕ1 > 49.5) and (ϕ1 < 49.52) and (ϕ2 < 40.5) and (ϕ2 > 40.48):
                Δv2 = [Δv2*cos(rad(β)), Δv2*sin(rad(β))]
                v = vec2Dadd(v, Δv2)
                postOrbit = True

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
