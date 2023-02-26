import matplotlib.pyplot as plt
import pandas as pd
plt.figure()
mps_per_element = 4
df = pd.read_csv("throughput.csv")
plt.plot(df["elements"]*mps_per_element,df["throughput"])
#plt.xscale("log")
#plt.yscale("log")
plt.legend()
plt.show()
