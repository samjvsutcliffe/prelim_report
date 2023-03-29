import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

markers = ["","x","o",".","<",">"]
linestyles = ["","--","-","-","-","-"]
df = pd.read_csv("shear.csv")
shear = df["shear"]
plt.figure()
for key,marker,ls in zip(df,markers,linestyles):
    if key != "shear":
        plt.plot(shear,df[key],label=key,ls=ls)
plt.legend()
plt.xlabel("Shear ratio")
plt.ylabel("Normalised shear stress")
plt.show()
