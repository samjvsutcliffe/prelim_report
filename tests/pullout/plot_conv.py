PDF_OUTPUT = True
import matplotlib as mpl
if PDF_OUTPUT:
    mpl.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
plt.close("all")
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
width = 3.487
height = width / 1.618

data_file = ""

df = pd.read_csv("conv_files{}/pullout.csv".format("_nonlocal"))
energy = df["energy"]
analytic_energy = energy.array[-1]
all_data = {}
for data_file in ["local","nonlocal"]:
    root_folder = "./conv_files_"
    df = pd.read_csv("{}{}/pullout.csv".format(root_folder,data_file))
    plt.figure(1)
    plt.plot(df["elements"],df["energy"],label=data_file)
    plt.xlabel("Elements")
    plt.ylabel("Energy")
    plt.figure(2)
    energy = df["energy"]
    energy_error = abs(energy - analytic_energy)/energy.array[-1]
    plt.plot(df["elements"],energy_error,label=data_file)
    origin = np.array([2,1])
    size = 2
    points = np.array([[1,1],[1,size],[size,1],[1,1]])
    points = (points*origin)
    plt.plot(points[:,0],points[:,1])
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Elements")
    plt.ylabel("Energy error")

    files = os.listdir("{}{}/".format(root_folder,data_file))
    finalcsv = re.compile("elements.*.csv")
    files_csvs = list(filter(finalcsv.match,files))
    numbers = re.compile("\d*")
    element_counts = [[int(y) for y in x if y][0] for x in map(numbers.findall,files_csvs)]
    lengths = sorted([[int(y) for y in x if y][0] for x in map(numbers.findall,files_csvs)])
    files_csvs = [x for _,x in sorted(zip(element_counts,files_csvs))]
    print("Notch lengths")
    print(lengths)

    max_stress = []
    stress_pos = []
    files = []
    all_dfs = []
    plt.figure(3)
    for dname in files_csvs:
        df = pd.read_csv("{}{}/{}".format(root_folder,data_file,dname))
        df = df[df["coord_y"]==df["coord_y"].min()]
        plt.plot(df["coord_x"],df["damage"],label=dname)
        all_dfs.append(df)
    plt.legend()
    plt.xlabel("X position")
    plt.ylabel("damage")
    all_data[data_file] = all_dfs
plt.figure(1)
plt.legend()
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
plt.figure(2)
plt.legend()
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
plt.savefig("pullout_conv.pdf")

plt.figure(4)
df = all_data["local"][-1]
x = df["coord_x"]
d = x * 0
d[(x>2) & (x<3)] = 0.1
plt.plot(x, d,label="Initial damage")
df = all_data["local"][-1]
plt.plot(df["coord_x"],df["damage"],label="Local")
df = all_data["nonlocal"][-1]
plt.plot(df["coord_x"],df["damage"],label="Nonlocal")
plt.legend()
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
plt.xlabel("X location (m)")
plt.ylabel("Damage")
plt.savefig("pullout_damage.pdf")
plt.show()

