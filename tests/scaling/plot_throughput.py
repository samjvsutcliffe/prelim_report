import matplotlib.pyplot as plt
import pandas as pd
plt.figure()
mps_per_element = 4
df = pd.read_csv("throughput.csv")
plt.plot(df["cores"],df["throughput"])
#plt.xscale("log")
#plt.yscale("log")
plt.xlabel("threads")
plt.ylabel("throughput")
plt.legend()
plt.figure()
plt.plot(df["cores"],1e3/df["throughput"])
plt.xlabel("threads")
plt.ylabel("time/1e3")
plt.legend()
plt.show()
