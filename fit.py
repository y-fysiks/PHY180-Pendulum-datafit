from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

time_tare = 33.692

data = pd.read_csv("data31.csv", delimiter = ', ')
time = data['time'].to_numpy() - time_tare
angle = data['angle'].to_numpy()

i_0 = 1.6441001553786583
p_0 = 0

def damped_harmonic_func(t, tau, T, p0):
    return i_0 * np.exp(-t/tau) * np.cos((2 * np.pi * (t/T)) + p0)

plt.plot(time, angle, 'bo', markersize = 1, label = 'data')

popt, pcov = curve_fit(damped_harmonic_func, time, angle)

plt.plot(time, damped_harmonic_func(time, *popt), 'r-', label = 'fit: tau=%5.3f, T=%5.3f, p0=%5.3f' % tuple(popt))

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()