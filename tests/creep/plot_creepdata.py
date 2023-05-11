import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

expdata = pd.read_csv("creep.csv")
df = pd.read_csv("output/creep.csv")
plt.plot(expdata["time"],expdata["damage"],label="0.93")
plt.plot(df["time"]/(60**2),df["damage"],label="mpm-0.93")
plt.xlabel("Time (h)")
plt.ylabel("Damage ()")
plt.legend()
plt.show()
