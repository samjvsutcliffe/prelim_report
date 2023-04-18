PDF_OUTPUT = True
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

df = pd.read_csv("output/far-field.csv")
plt.figure(1)
H = 125
plt.plot(df["y"]/H,df["s_xx"]*1e-6,label="MPM")
plt.plot(df["y"]/H,df["s_an"]*1e-6,label="Analytic")
plt.xlabel("Normalised height ()")
plt.ylabel("$\sigma_{xx}$ ($MPa$)")
plt.legend()

plt.gcf().subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
plt.gcf().set_size_inches(width, height)
if PDF_OUTPUT:
    plt.savefig("slump_analytic_stress.pdf")
plt.show()


