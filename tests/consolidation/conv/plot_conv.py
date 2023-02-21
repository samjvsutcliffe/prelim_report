import matplotlib.pyplot as plt
import pandas as pd
plt.figure()
for name in ["mpm","fs"]:
    df = pd.read_csv("convergance_{}.csv".format(name))
    plt.plot(df["elements"],df["error"],label=name)
plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()
