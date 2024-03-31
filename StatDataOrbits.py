import matplotlib.pyplot as plt

G = 6.674e-11
M = 1.98855e30
m = 5.972e24

a = []
v = []
r = []
L = [0 for _ in range(759)]

statFile = open('./statDataHyperbOrbit.txt', 'r')
for i in range(759):
    a += ['']
    v += ['']
    r += ['']
    while True:
        temp = statFile.read(1)
        if temp == '\n':
            break
        else:
            a[i] += temp
    while True:
        temp = statFile.read(1)
        if temp == '\n':
            break
        else:
            v[i] += temp
    while True:
        temp = statFile.read(1)
        if temp == '\n':
            break
        else:
            r[i] += temp
    a[i] = float(a[i])
    v[i] = float(v[i])
    r[i] = float(r[i])
    L[i] = m*(v[i]**2/2+G*M/r[i])

statFile.close()

y = [x for x in range(759)]

f1 = plt.figure('Hyperbolic Orbit')

plt.subplot(1, 3, 1)
plt.plot(y, a, color='yellow')
plt.title('Acceleration')
plt.subplot(1, 3, 2)
plt.plot(y, v, color='orange')
plt.title('Speed')
plt.subplot(1, 3, 3)
plt.plot(y, r, color='blue')
plt.title('Distance')

plt.subplots_adjust(wspace=0.5)

f2 = plt.figure('Lagrangian of Hyperbolic Orbit')
plt.plot(y, L, color='red')

#--------------------------------------------------------------------------------

a = []
v = []
r = []
L = [0 for _ in range(549)]

statFile = open('./statDataEarthOrbit.txt', 'r')
for i in range(549):
    a += ['']
    v += ['']
    r += ['']
    while True:
        temp = statFile.read(1)
        if temp == '\n':
            break
        else:
            a[i] += temp
    while True:
        temp = statFile.read(1)
        if temp == '\n':
            break
        else:
            v[i] += temp
    while True:
        temp = statFile.read(1)
        if temp == '\n':
            break
        else:
            r[i] += temp
    a[i] = float(a[i])
    v[i] = float(v[i])
    r[i] = float(r[i])
    L[i] = m*(v[i]**2/2+G*M/r[i])

statFile.close()

y = [x for x in range(549)]

f3 = plt.figure('Earth Orbit')

plt.subplot(3, 1, 1)
plt.plot(y, a, color='yellow')
plt.ylabel('a')
plt.title('Acceleration')
plt.subplot(3, 1, 2)
plt.plot(y, v, color='orange')
plt.ylabel('v')
plt.title('Speed')
plt.subplot(3, 1, 3)
plt.plot(y, r, color='blue')
plt.ylabel('r')
plt.title('Distance')

plt.subplots_adjust(hspace=0.5)

f4 = plt.figure('Lagrangian of Earth Orbit')
plt.plot(y, L, color='green')

plt.show()

# 549 for earth orbit
