import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

E = 1e6
L = 50
g = 10
rho = 800

def calculate_f(y):
    f = 1
    epsilon = 1
    while np.any(epsilon > 1e-10):
        #print("f: {}, eps: {}".format(f,epsilon))
        f_new = f - (((E/f) * np.log(f))-stress(y))/(E*(1-np.log(f))/(np.power(f,2)))
        epsilon = np.abs(f_new - f)
        f = f_new
    return f

def stress(y):
    return -rho * g * (L - y)

step = 0.1
y = np.arange(0,L,step)
dy = np.ones(y.shape) * step
y_int = np.zeros(y.shape)

plt.ion()
plt.close("all")
plt.figure()
f = calculate_f(y)

for i in range(0,len(dy)):
    for j in range(0,i):
        y_int[i] += dy[j]*f[j]
plt.plot(-stress(y),y_int,label="Analytic")

for name in ["mpm","gimp","mpmfs","gimpfs"]:
    df = pd.read_hdf("particles_{}.h5".format(name))
    min_x = df["coord_x"].min()
    ids = df["coord_x"] < min_x + 1e-5
    plt.scatter(-df["stress_yy"][ids],df["coord_y"][ids],label=name)
plt.xlabel("Stress (Pa)")
plt.ylabel("Height (m)")
plt.legend()
plt.ylim([0,L+5])

