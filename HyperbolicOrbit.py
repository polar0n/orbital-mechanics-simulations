import tkinter as tk
from tkinter import font
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

oneCmplRot = False                  # Flag shows if satellite did at least one full orbit


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


sat = Turtle()                  # Satellite turtle

sat.color('white', 'black')     # Initialise our satellite
bgcolor('black')
sat.speed(0)
tracer(0, 0)
sat.pu()
sat.fd(2)
sat.lt(90)
sat.begin_poly()
sat.circle(2)
sat.end_poly()
m1 = sat.get_poly()
planetshape = Shape("compound")
planetshape.addcomponent(m1, "gray")
register_shape("planet", planetshape)
sat.color('blue', 'black')
sat.pu()
sat.home()
sat.dot(10)
sat.color('white', 'black')
sat.shape('planet')

v[0] += dt * a[0]                               # First step in evolution of satellite position
r = [r[0] + dt * v[0], r[1] + dt * v[1]]
sat.setpos(pixels2D(r))

sat.pd()

# Get user choice regarding show of telemetry data
telemetryFlag = numinput('Telemetry',
                         'No telemetry: 0\nConsole telemetry: 1\nOnscreen telemetry: 2',
                         0, minval=0, maxval=2)

if telemetryFlag == 2:
    Dosis = font.Font(family='Dosis', size=15)
    linespace = Dosis.metrics('linespace')

    root = getcanvas()
    telemetry = root.create_text(5-window_width()/2, -window_height()/2,
                                 fill='white', font=Dosis, anchor=tk.NW)
    root.pack()

i = 2                   # 2, because we already did first step
try:    
    while True:
        if not oneCmplRot:  # If satellite did not make any full rotations
            b = a[1]        # Register the last acceleration for further determination of one complete orbit
        a = [-G*M*r[0]/pow(vec2DLength(r), 3), -G*M*r[1]/pow(vec2DLength(r), 3)]
        v = [v[0] + i*dt*a[0], v[1] + i*dt*a[1]]
        r = [r[0] + i*dt*v[0], r[1] + i*dt*v[1]]
        sat.setpos(pixels2D(r))
    
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
    
        if (not oneCmplRot) and (b > 0.0) and (a[1] <= 0.0):            # Check if satellite did one full rotation
            oneCmplRot = True                                           # If sat did no rotation and if it's
                                                                        # previous position was -Yaxis
                                                                        # and if present position is +Yaxis
                                                                        # then set one rotationflag to true
        if oneCmplRot and (round(r[1], 1) == round(vec2DLength(r), 1)): # Check if sat did one rotation and if normal anomaly is 90 degrees
            v[0] = -11760                                               # then give the satellite a 
                                                                        # burnout boost to escape earth's gravitational field
    
        if (-window_height()/2+50) > sat.ycor():                        # If satellite approached the
            exitonclick()                                               # window edge then stop simulation
    
        i += 1
        if i == 60000:
            i -= 900
except Exception:
    pass