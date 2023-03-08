import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt


E = 1e6
L = 50
g = 10
rho = 80


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
y_int_0 = np.zeros(y.shape)
y_int = np.zeros(y.shape)

#plt.ion()
plt.close("all")
plt.figure()
f = calculate_f(y)

for i in range(0,len(dy)):
    for j in range(0,i):
        y_int_0[i] += dy[j]
        y_int[i] += dy[j]*f[j]
plt.plot(-stress(y),y_int,label="Analytic")
plt.figure(0)

data_name = ""
data_dir = "./conv_files/"
files = os.listdir(data_dir)
p = re.compile(".*\.csv")
files = list(filter(p.match,files))
numbers = re.compile("\d+")
files.sort(key=lambda x:int(numbers.findall(x)[0]))
data = []
error = []
elements = []
print(files)
for name in files:
    elements.append(int(numbers.findall(name)[0]))
for name in files:
    df = pd.read_csv("./{}/{}".format(data_dir,name))
    min_x = df["coord_x"].min()
    ids = df["coord_x"] < (min_x + 1e-5)
    data.append(df[ids])
    #print("File:{}, rms vel:{}".format(name,df["velocity_y"].abs().mean()))


#plt.figure()
#for df,name in zip(data,files):
#    plt.scatter(-df["stress_yy"][ids],df["coord_y"][ids],label=name)
#plt.plot(-stress(y),y_int)
#plt.xlabel("Stress (Pa)")
#plt.ylabel("Height (m)")
#plt.legend()
#plt.ylim([0,L+5])

plt.figure()
plt.title("Initial configuration")
for name,df,e in zip(files,data,elements):
    h = L/e
    y_final = df["coord_y"]
    mps = len(df["coord_y"])
    v_0 = L*h / (mps)
    y_0 = (L/(mps+1))*np.arange(1,mps+1)
    #plt.plot(-stress(y_0),y_0)
    e = np.sum(abs(stress(y_0) - df["stress_yy"]) * v_0/(L*h*L*rho*g))
    error.append(e)
    #analytic_interp = np.interp(y_final,y_int,stress)
    plt.scatter(-df["stress_yy"],y_0,label=name)
plt.plot(-stress(y_0),y_0)
#plt.scatter(-stress(y_0),y_0)
    



plt.xlabel("Stress (Pa)")
plt.ylabel("Height (m)")
plt.legend()
plt.ylim([0,L+5])
convergance = pd.DataFrame({"elements":elements,"error":error})
plt.figure(0)
plt.title("Conv")
plt.plot(elements,error,"-o",label=data_name)
plt.legend()
plt.xlabel("Elements")
plt.ylabel("Stress error")
plt.xscale("log")
plt.yscale("log")
#Linear convergance
origin = np.array([2,0.01])
size = 2
points = np.array([[1,1],[1,size],[size,1],[1,1]])
points = (points*origin)
plt.plot(points[:,0],points[:,1])
#Quadratic
origin = np.array([100,0.01])
size = 2
points = np.array([[1,1],[1,2*size],[size,1],[1,1]])
points = (points*origin)
plt.plot(points[:,0],points[:,1])
plt.show()


