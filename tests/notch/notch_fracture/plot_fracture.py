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
# plt.rc('text', usetex=True)
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

bindings = [0,10,11,15, 40]
#bindings = range(0,60,1)
fig,axs = plt.subplots(len(bindings),1)
for frame,i in enumerate(bindings):
    ax = axs[frame]
    #fig = plt.figure()
    #ax = fig.add_subplot(111,aspect="equal")
    df = full_data[i]
    patch_list=[]
    #plt.plot([])
    #plt.scatter(df["coord_x"],df["coord_y"],c="b")
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"]-300,
                                     df["lx"],
                                     df["ly"],
                                     df["damage"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly)
#            linewidth=1,fill=True)
        patch_list.append(patch)
        #ax.add_patch(patch)
#    for patch,damage in zip(patch_list,df["damage"]):
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    p.set_array(df["eps"]*1e-6)
    ax.add_collection(p)
    #fig.colorbar(p,location="bottom")
    ax.set_xlim([0,1100])
    ax.set_ylim([-220,30])
    ax.label_outer()
    #plt.xlim([0,1100])
    #plt.ylim([100,330])
    #plt.savefig("outframes/frame_{:05}.png".format(i))
    #plt.savefig("stress_states_{:05}.pdf".format(i))
    #p.set_clim([0,1])
    #plt.close("all")

# plt.xlim([0,1100])
# plt.ylim([100,330])
plt.savefig("combined.pdf".format(i))

for frame,i in enumerate(bindings):
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect="equal")
    df = full_data[i]
    patch_list=[]
    #plt.plot([])
    #plt.scatter(df["coord_x"],df["coord_y"],c="b")
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"]-300,
                                     df["lx"],
                                     df["ly"],
                                     df["damage"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly)
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    p.set_array(df["eps"]*1e-6)
    ax.add_collection(p)
    fig.colorbar(p,location="bottom")

    ax.set_xlim([0,1100])
    ax.set_ylim([-210,40])
    #plt.savefig("outframes/frame_{:05}.png".format(i))
    plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    plt.gcf().set_size_inches(width, height)
    plt.savefig("stress_states_{:05}.pdf".format(i))
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
                                     df["coord_y"]-300,
                                     df["lx"],
                                     df["ly"],
                                     df["damage"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly)
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    p.set_array(df["damage"])
    ax.add_collection(p)
    fig.colorbar(p,location="bottom")

    ax.set_xlim([0,1100])
    ax.set_ylim([-210,40])
    #plt.savefig("outframes/frame_{:05}.png".format(i))
    plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    plt.gcf().set_size_inches(width, height)
    plt.savefig("damage_states_{:05}.pdf".format(i))
    #p.set_clim([0,1])
    #plt.close("all")

def anim(j):
    i = bindings[j%len(bindings)]
    df = full_data[i]
    plt.cla()
    plt.scatter(df["coord_x"],df["coord_y"],c=df["damage"])
    plt.xlim([400,1100])
    plt.ylim([100,340])

#plt.ion()
# fig = plt.figure()
# ani = animation.FuncAnimation(fig, anim, interval=500,repeat=False) 
plt.show()
