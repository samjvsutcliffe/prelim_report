PDF_OUTPUT = False
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

data = pd.read_csv("load-disp.csv")

mpm = pd.read_csv("output/disp.csv")

plt.figure()
plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
plt.plot(data["disp"],data["load"],label="Experimental")
plt.plot(-1e3 * mpm["disp"],0.1 * mpm["load"],label="MPM")
plt.xlabel("Displacement (mm)")
plt.ylabel("Load (N)")
plt.legend()
plt.savefig("load-disp-graph.pdf")
plt.show()
