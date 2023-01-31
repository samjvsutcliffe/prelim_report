import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
plt.figure()
def evaluate_data(data_dir):
    files = os.listdir(data_dir)
    dt = 1e-2
    p = re.compile('simcsv.*\.csv') 
    h5_files = [f for f in files if p.match(f)]
    max_stress = []
    damage = []
    time = []
    for f in h5_files:
        df = pd.read_csv(data_dir+f)
        max_stress.append(df["stress_1"].max())
        damage.append(df["damage"].max())
        time.append(dt * 100 * float(re.findall("\d+",f)[0]))
    time = np.array(time)
    max_stress = np.array(max_stress)
    damage = np.array(damage)
    return pd.DataFrame({"time":time,"stress_1":max_stress,"damage":damage})
df_elastic = evaluate_data("./output_elastic/")
df_viscous = evaluate_data("./output_viscous/")
plt.figure()
plt.plot(df_elastic["time"],df_elastic["stress_1"]/1e6,label="stress 1")
plt.plot(df_viscous["time"],df_viscous["stress_1"]/1e6,label="stress 1")
plt.legend()
plt.figure()
plt.plot(df_elastic["time"],df_elastic["damage"],label="damage")
plt.plot(df_viscous["time"],df_viscous["damage"],label="damage")
plt.legend()
plt.show()

