import tkinter as tk
from tkinter import font
from turtle import *
from math import pow, sqrt
from os import system as sys

G = 6.674e-11                       # Gravitational Constant
scaleFactor = 1495980230/2          # meters/pixel
r = [147.095e9, 0]                  # Earth's periapsis
M = 1.98855e30                      # Sun's mass
semiMajorAxis = 149598023000
a = [-G*M*r[0]/pow(r[0], 3), 0]
v = [0, 30300]                      # meters/second
dt = 0.005                          # time portions


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


earth = Turtle()

earth.color('white', 'black')
bgcolor('black')
earth.speed(0)
tracer(0, 0)
earth.pu()
earth.fd(6)
earth.lt(90)
earth.begin_poly()
earth.circle(6, 180)
earth.end_poly()
m1 = earth.get_poly()
earth.begin_poly()
earth.circle(6, 180)
earth.end_poly()
m2 = earth.get_poly()
planetshape = Shape("compound")
planetshape.addcomponent(m1, "blue")
planetshape.addcomponent(m2, "green")
register_shape("planet", planetshape)
earth.color('yellow', 'black')
earth.dot(35)
earth.color('white', 'black')
earth.shape('planet')
earth.pu()

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
earth.setpos(pixels2D(r))

earth.pd()

# 2, because we already did first step
i = 2
try:
    while True:
        a = [-G*M*r[0]/pow(vec2DLength(r), 3), -G*M *
             r[1]/pow(vec2DLength(r), 3)]
        v = [v[0] + i*dt*a[0], v[1] + i*dt*a[1]]
        r = [r[0] + i*dt*v[0], r[1] + i*dt*v[1]]
        earth.setpos(pixels2D(r))

        if (i % 150) == 0:                  # Make a screen update once in 150 cycles of i
            if telemetryFlag == 1:          # Telemetry flag is set to 'Terminal Telemetry'
                sys('cls')
                print('a =', round(vec2DLength(a), 6), 'm/s^2')
                print('v =', round(vec2DLength(v), 4), 'm/s')
                print('r =', round(vec2DLength(r), len(str(dt))), 'm')

            if telemetryFlag == 2:          # Telemetry flag is set to 'On-Screen Telemetry'
                root.itemconfigure(telemetry, text='a = ' +
                                   str(round(vec2DLength(a), 2)) +
                                   ' m/s^2\n' + 'v = ' +
                                   str(round(vec2DLength(v), 2)) +
                                   ' m/s\n' + 'r = ' +
                                   str(round(vec2DLength(r)*1e-3, 2)) + ' km\n')

            update()        # Update the canvas (drawing scene)

        i += 1

        # Fix the i value so it cannot cause lag by being
        # too big. -150 because that's the screen update rate.
        if i == 60000:
            i = i - 900
except Exception:
    pass
