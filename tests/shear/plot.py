PDF_OUTPUT = False
import matplotlib as mpl
if PDF_OUTPUT:
    mpl.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
width = 3.487
height = width / 1.618

markers = ["","x","o",".","<",">"]
linestyles = ["","--","-","-","-","-"]
df = pd.read_csv("shear.csv")
shear = df["shear"]
labels = ["","Analytic","Rate-less","SS","Logspin","Jaumann"]
plt.figure()
for key,marker,ls,l in zip(df,markers,linestyles,labels):
    if key != "shear":
        plt.plot(shear,df[key],label=l,ls=ls)
plt.legend()
plt.xlabel("Shear ratio")
plt.ylabel("Normalised shear stress")
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
# plt.savefig("shear.png")
plt.savefig("shear.pdf")
plt.show()
