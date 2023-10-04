from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import fit_black_box as fbb

time_tare = 33.692

data = pd.read_csv("data31.csv", delimiter = ', ')
time = data['time'].to_numpy() - time_tare
angle = data['angle'].to_numpy()

i_0 = 1.6441001553786583
p_0 = 0

def damped_harmonic_func(t, i0, tau, T, p0):
    return i0 * np.exp(-t/tau) * np.cos((2 * np.pi * (t/T)) + p0)

cutoff = np.deg2rad(20)
for i in range(len(angle) - 1, -1, -1):
    if (angle[i] > cutoff):
        for j in range(i, -1, -1):
            angle = np.delete(angle, 0)
            time = np.delete(time, 0)
        time_tare = time[0]

        break
time = time - time_tare

time_error = np.full(shape=time.size, fill_value=0.05)

angle_error = np.full(shape=time.size, fill_value=np.deg2rad(0.15))

fbb.plot_fit(damped_harmonic_func, time, angle, xerror=time_error, yerror=angle_error, xlabel="Time (s)", ylabel="Angle (rad)", title="Amplitude vs Time")


# plt.plot(time, angle, 'bo', markersize = 1, label = 'data')

# popt, pcov = curve_fit(damped_harmonic_func, time, angle)

# plt.plot(time, damped_harmonic_func(time, *popt), 'r-', label = 'fit: i0: %5.3f, tau=%5.3f, T=%5.3f, p0=%5.3f' % tuple(popt))

# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.show()