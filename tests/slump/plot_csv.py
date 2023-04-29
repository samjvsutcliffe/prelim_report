PDF_OUTPUT = False
import matplotlib as mpl
if PDF_OUTPUT:
    mpl.use('pdf')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm
import re
import os
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
width = 3.487
height = width / 1.618

plt.close("all")
output_dir = "./output/"
files = os.listdir(output_dir)
finalcsv = re.compile("sim.*.csv")
files_csvs = list(filter(finalcsv.match,files))
dt = 0.5e0
time = []
max_stress = []
damage = []
full_data = []
for i,dname in enumerate(files_csvs):
    df = pd.read_csv(output_dir+"{}".format(dname))
    s1 = df["stress_xx"].mean()
    max_stress.append(s1)
    damage.append(df["damage"].mean())
    time.append(i*dt)
    full_data.append(df)

ff_ids = full_data[0]["coord_x"] <= full_data[0]["coord_x"].min()
plt.figure()
df = full_data[-1]
H = 100
rho = 900
g = 9.8
nu = 0.325
y = df["coord_y"][ff_ids]
s_an = (nu/(1-nu)) * (rho * g * (y - (H * 0.5)))
scale = 1e-6
plt.plot(df["coord_y"][ff_ids],df["stress_xx"][ff_ids]*scale,label="mpm",marker="x")
plt.plot(y,s_an*scale,label="analytic")
plt.legend()
plt.xlabel("Normalised height")
plt.ylabel("Longtitudinal stress $\sigma_{xx}$ (MPa)")
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
plt.savefig("sxx_analytic.pdf")


length_plot = 2100

bindings = [0, 25, 50 , 75 , 100]
bindings = [i for i in bindings if i < len(full_data)]

for frame,i in enumerate(bindings):
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect="equal")
    df = full_data[i]
    patch_list=[]
    #plt.plot([])
    #plt.scatter(df["coord_x"],df["coord_y"],c="b")
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"],
                                     df["lx"],
                                     df["ly"],
                                     df["damage"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly)
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    #p.set_array(df["stress_xx"]*1e-6)
    p.set_array(df["tau_xy"]*1e-6)
    ax.add_collection(p)
    fig.colorbar(p,location="bottom",label= "$\sigma_{xy}$")

    ax.set_xlim([0,length_plot])
    ax.set_ylim([0,110])
    #plt.savefig("outframes/frame_{:05}.png".format(i))
    plt.gcf().subplots_adjust(left=.08, bottom=.22, right=.95, top=.95)
    plt.gcf().set_size_inches(width, width/2.0)
    # plt.savefig("shear_stress_{:05}.pdf".format(i))
    plt.savefig("stress_xy.pdf")
    #p.set_clim([0,1])
    #plt.close("all")

for frame,i in enumerate(bindings):
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect="equal")
    df = full_data[i]
    patch_list=[]
    #plt.plot([])
    #plt.scatter(df["coord_x"],df["coord_y"],c="b")
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"],
                                     df["lx"],
                                     df["ly"],
                                     df["damage"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly)
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    #p.set_array(df["stress_xx"]*1e-6)
    p.set_array(df["stress_xx"]*1e-6)
    ax.add_collection(p)
    fig.colorbar(p,location="bottom",label= "$\sigma_{xx}$")

    ax.set_xlim([0,length_plot])
    ax.set_ylim([0,110])
    #plt.savefig("outframes/frame_{:05}.png".format(i))
    plt.gcf().subplots_adjust(left=.08, bottom=.22, right=.95, top=.95)
    plt.gcf().set_size_inches(width, width/2.0)
    plt.savefig("stress_xx_{:05}.pdf".format(frame))
    #p.set_clim([0,1])
    #plt.close("all")

def anim(j):
    i = bindings[j%len(bindings)]
    df = full_data[i]
    plt.cla()
    plt.scatter(df["coord_x"],df["coord_y"],c=df["damage"])
    plt.xlim([400,length_plot])
    plt.ylim([100,340])

#plt.ion()
# fig = plt.figure()
# ani = animation.FuncAnimation(fig, anim, interval=500,repeat=False) 
plt.show()
