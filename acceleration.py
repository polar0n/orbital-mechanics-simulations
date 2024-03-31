#!/usr/bin/env python3

from math import sqrt

#We have a satellite on low earth orbit(160km<h<2000km) h = 250km = 25e4m from earth
#Which have mass of 770kg's

#constants
M = 5.98e24 #[kg] earth's mass
m = 770 #[kg] satellite's mass
height = 25e4 #[m] satellite's height
Rp = 6.3674447e6 #[m] earth's average radius
R = height + Rp #[m] distance from center of earth to satellite
G = 6.67e-11 #[Nm^2/kg^2] gravitational constant
g = 9.807 #[m/s^2] acceleration due to gravity of earth

#calculations
F = G * ((M * m)/pow(R, 2)) #law of universal atraction
print('(1)Gravitational interaction between earth and satellite:', F, 'N')

a2 = F / m #second Newton's law
print('(2.1)Satellite\'s acceleration towards earth:', a2, 'm/s^2')

a1 = F / M #second Newton's law
print('(2.2)Earth\'s acceleration towards satellite:', a1, 'm/s^2')

gh = g * pow(R, 2)/pow(R + height, 2) #Formula of gravitational acceleration at certain height
print('(3)Earth\'s gravitational acceleration at', 25e4, 'm:', gh, 'm/s^2')

gh = (G*M)/pow(R, 2)
print('(1->2=4)Earth\'s gravitational acceleration at', 25e4, 'm:', gh, 'm/s^2')

v = sqrt((G*M)/R)
print('(5.1)Speed of satellite on a circular earth orbit:', v, 'm/s')

v = sqrt((F*R)/m)
print('(5.2)Speed of satellite on a circular earth orbit:', v, 'm/s')

input()