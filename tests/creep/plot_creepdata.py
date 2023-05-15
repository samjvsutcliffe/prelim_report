import matplotlib as mpl
PDF_OUTPUT = True
if PDF_OUTPUT:
    mpl.use('pdf')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)
width = 3.487
height = width / 1.618

expdata = pd.read_csv("creep.csv")
df = pd.read_csv("output/creep.csv")
plt.plot(expdata["time"],expdata["damage"],label="0.93MPa MPM")
plt.plot(df["time"]/(60**2),df["damage"],label="0.93MPa Experimental")
plt.xlabel("Time (h)")
plt.ylabel("Damage ()")
plt.legend()
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
plt.savefig("creep.pdf")
plt.show()
