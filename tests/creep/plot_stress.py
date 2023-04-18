import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

output_dir = "./output/"
files = os.listdir(output_dir)
finalcsv = re.compile("sim.*.csv")
files_csvs = list(filter(finalcsv.match,files))
dt = 0.5e0
time = []
max_stress = []
damage = []
for i,dname in enumerate(files_csvs):
    df = pd.read_csv(output_dir+"{}".format(dname))
    s1 = df["stress_xx"].mean()
    max_stress.append(s1)
    damage.append(df["damage"].mean())
    time.append(i*dt)

critical_stress = 0.2e6
time_period = 8
time = np.array(time)
damage = np.array(damage)
max_stress = np.array(max_stress)
plt.figure(1)
plt.xlabel("N")
plt.plot(time/time_period,max_stress/critical_stress,"-o")
plt.figure(2)
plt.xlabel("N")
plt.plot(time/time_period,damage,"-o")
plt.figure(3)
plt.xlabel("Time")
plt.plot(time,max_stress/critical_stress,"-o")
plt.figure(4)
plt.xlabel("Time")
plt.plot(time,damage,"-o")
plt.show()
