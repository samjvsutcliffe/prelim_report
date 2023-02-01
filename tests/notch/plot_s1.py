import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
plt.figure()
def evaluate_data(data_dir):
    files = os.listdir(data_dir)
    dt = 1e-2
    p = re.compile('simcsv.*\.vtk') 
    h5_files = [f for f in files if p.match(f)]
    max_stress = []
    damage = []
    time = []
    if len(h5_files) > 0:
        print("Found files")
    for f in h5_files:
        df = pd.read_csv(data_dir+f)
        max_stress.append(df["stress_1"].max())
        damage.append(df["damage"].max())
        time.append(dt * 100 * float(re.findall("\d+",f)[0]))
    time = np.array(time)
    max_stress = np.array(max_stress)
    damage = np.array(damage)
    return pd.DataFrame({"time":time,"stress_1":max_stress,"damage":damage})
df_elastic = evaluate_data("./notch_nodamage/notch_elastic/output/")
df_viscous = evaluate_data("./notch_nodamage/notch_viscous/output/")
plt.figure()
plt.xlabel("Time s?")
plt.ylabel("Sigma 1")
plt.plot(df_elastic["time"],df_elastic["stress_1"]/1e6,label="elastic")
plt.plot(df_viscous["time"],df_viscous["stress_1"]/1e6,label="viscous")
plt.legend()
plt.figure()
plt.plot(df_elastic["time"],df_elastic["damage"],label="elastic")
plt.plot(df_viscous["time"],df_viscous["damage"],label="viscous")
plt.xlabel("Time s?")
plt.ylabel("Damage")
plt.legend()
plt.show()

