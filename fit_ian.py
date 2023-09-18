from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

angle_tare = 0

data = pd.read_csv(r"data31.csv", delimiter = ', ')
time = data['time'].to_numpy()
angle = data['angle'].to_numpy() + angle_tare
print(time)
print(np.shape(time))

i_0 = 0.746
phi_0 = 0

def linear_reg(t, m, b):
    return m*t + b

def local_m(time, angle):
    local_mms = []
    time_arr = []
    for i in range(time.size - 2):
        if(((angle[i + 1] - angle[i]) < 0) & ((angle[i] - angle[i - 1]) > 0)):
            local_mms.append(np.abs(angle[i]))
            time_arr.append(time[i])

    return [time_arr, local_mms]

def angle_func(t, tau, T, A):
    return i_0 * np.exp(-t/tau) * np.cos((2 * np.pi * (t/T)) + phi_0) - A

def period_func(o, t_o, b, c):
    pass

plt.plot(time, angle, 'bo', markersize = 1, label = 'data')
popt, pcov = curve_fit(angle_func, time, angle)
plt.plot(time, angle_func(time, *popt), 'r-', label = 'fit: tau=%5.3f, T=%5.3f, A=%5.3f' % tuple(popt))
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

# test = local_m(time, angle)
# print(test)

# plt.plot(test[0], np.log(test[1]), 'ro', label = 'data')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.show()