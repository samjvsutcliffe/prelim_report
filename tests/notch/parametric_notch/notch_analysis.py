PDF_OUTPUT = False
import matplotlib as mpl
if PDF_OUTPUT:
    mpl.use('pdf')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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


scale = np.array([200,300])
for name,s in zip(["elastic","viscous"],scale):
    output_dir = "./output_notch_{}/".format(name)

    files = os.listdir(output_dir)
    finalcsv = re.compile("final.*.csv")
    files_csvs = list(filter(finalcsv.match,files))
    numbers = re.compile("\d*")
    lengths = sorted([[int(y) for y in x if y][0] for x in map(numbers.findall,files_csvs)])
    print("Notch lengths")
    print(lengths)

    max_stress = []
    stress_pos = []
    for dname in lengths:
        df = pd.read_csv(output_dir+"/final_{}.csv".format(dname))
        #plt.scatter(df["coord_x"],df["coord_y"],label=dname)
        #plt.legend()
        s1 = df["eps"].max()
        max_stress.append(s1)
        stress_pos.append(df["coord_x"][df["eps"]==s1])
    lengths = np.array(lengths)
    max_stress = np.array(max_stress)
    stress_pos = np.array(stress_pos)
    plt.figure(2)
    plt.plot(lengths,max_stress*1e-6,"-o",label=name)
    plt.figure(3)
    plt.plot(lengths,2000-stress_pos,"-o",label=name)

width = 3.487
height = width / 1.618

plt.figure(2)
#plt.plot(lengths,max_stress*1e-6,"-o")
plt.xlabel("Notch length ($m$)")
plt.ylabel("EPS ($MPa$)")
plt.legend()
plt.axhline(0.2,c="r",ls="--")

plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
if PDF_OUTPUT:
    plt.savefig("bench_stress.pdf")
plt.figure(3)
#plt.plot(lengths,2000-stress_pos,"-o")
plt.xlabel("Notch length (m)")
plt.ylabel("Max EPS distance from front")
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
if PDF_OUTPUT:
    plt.savefig("bench_distance.pdf")
plt.show()


