PDF_OUTPUT = False
import matplotlib as mpl
if PDF_OUTPUT:
    mpl.use('pdf')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm
import os
import re


plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

# width as measured in inkscape
width = 3.487
height = width / 1.618

output_dir = "./output_notch/"

plt.figure(1)
plt.figure(2)

scale = np.array([200])
for name,s in zip(["200"],scale):
    output_dir = "./output_notch/".format(name)

    #files = os.listdir(output_dir)
    #finalcsv = re.compile("final.*.csv")
    #files_csvs = list(filter(finalcsv.match,files))
    #numbers = re.compile("\d*")
    #lengths = sorted([[int(y) for y in x if y][0] for x in map(numbers.findall,files_csvs)])
    #lengths_mpm = lengths
    #print("Notch lengths")
    #print(lengths)

    #max_stress = []
    #eps_stress = []
    #stress_pos = []
    #for dname in lengths:
    #    df = pd.read_csv(output_dir+"/final_{}.csv".format(dname))
    #    bottom_ids = df["coord_y"] < 250
    #    tau_xx = df["stress_xx"] - (0.5 * (df["stress_xx"] + df["stress_yy"]))
    #    s1 = tau_xx[bottom_ids].max()
    #    pos = df["coord_x"][tau_xx==s1].iat[0]
    #    print(pos)
    #    max_stress.append(s1)
    #    eps_stress.append(df["eps"].max())
    #    stress_pos.append(pos)
    #    #plt.figure()
    #    #plt.scatter(df["coord_x"],df["coord_y"],c=df["eps"]*1e-6,label=dname)
    #    #plt.axvline(x=pos)
    #    #plt.colorbar()
    #    #plt.legend()
    df = pd.read_csv(output_dir+"notch_txx.csv")
    lengths = np.array(df["length"])
    lengths_mpm = lengths
    max_stress = np.array(df["txx"])
    stress_pos = np.array(df["x"])
    print("{}: {}".format(name,8000-stress_pos[-1]))
    name = "MPM"
    max_stress *= 1e-6
    #lengths /= s
    #max_stress /= s * 1000 * 9.8
    plt.figure(1)
    plt.plot(lengths,max_stress,"-o",label=name)
    plt.figure(2)
    plt.plot(lengths,8000-stress_pos,"-o",label=name)

width = 3.487
height = width / 1.618

plt.figure(1)
#plt.plot(lengths,max_stress*1e-6,"-o")
#plt.plot(lengths,max_stress,"-o",label=name)
plt.xlabel("Notch length ($m$)")
plt.ylabel("EPS ($MPa$)")
plt.legend()
plt.axhline(0.33,c="r",ls="--")

plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
if PDF_OUTPUT:
    plt.savefig("bench_stress.pdf")
plt.figure(2)
data = [734, 509 , 320 , 248 , 219 , 213]
lengths = [0,10,25,50,75,100]
plt.plot(lengths,data,"-o",label="2D Mosbeux")
plt.legend()
plt.xlabel("Notch length (m)")
plt.ylabel("Max EPS distance from front")
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
if PDF_OUTPUT:
    plt.savefig("bench_distance.pdf")

print("Mos: {}".format(data[-1]))

bindings = [100]
for frame,i in enumerate(bindings):
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect="equal")
    df = pd.read_csv(output_dir+"/final_{}.csv".format(int(i)))

    #patch = Rectangle(xy=(0,0) ,width=6000, height=-300,color="blue")
    #patch_sea = [patch]
    #ps = PatchCollection(patch_sea)
    #ax.add_collection(ps)

    patch_list=[]
    for a_x, a_y,lx,ly,damage in zip(df["coord_x"],
                                     df["coord_y"]-300,
                                     df["lx"],
                                     df["ly"],
                                     df["damage"]):
        patch = Rectangle(
            xy=(a_x-lx/2, a_y-ly/2) ,width=lx, height=ly)
        patch_list.append(patch)
    p = PatchCollection(patch_list, cmap=cm.jet, alpha=1)
    tau_xx = df["stress_xx"] - (0.5 * (df["stress_xx"] + df["stress_yy"]))
    eps = df["eps"]
    p.set_array(tau_xx*1e-6)
    ax.add_collection(p)
    fig.colorbar(p,location="bottom",label="EPS ($MPa$)",pad=0.2)


    ax.set_xlim([0,1020])
    ax.set_ylim([-210,40])
    #plt.savefig("outframes/frame_{:05}.png".format(i))
    plt.gcf().subplots_adjust(left=.15, bottom=.28, right=.95, top=1.0)
    figure_aspect = 0.5
    plt.gcf().set_size_inches(width, width * figure_aspect)
    plt.savefig("stress_bench.pdf".format(i))
plt.show()


