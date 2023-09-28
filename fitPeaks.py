from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import fit_black_box as fbb

time_tare = 9.487

data = pd.read_csv("data33.csv", delimiter = ', ')
timeRaw = data['time'].to_numpy() - time_tare
angleRaw = data['angle'].to_numpy()

time = []
angle = []
prevAngle = 0
for i in range(0, angleRaw.size - 1):
    k = i
    if angleRaw[i] <= np.deg2rad(80) and angleRaw[i] >= np.deg2rad(2):

        if (prevAngle !=angleRaw[i - 1]):
            print(str(i) + " " + str(angleRaw[i - 1]) + " " + str(prevAngle))
        if(angleRaw[i] >= 0):
            if(angleRaw[i] > prevAngle):

                if (angleRaw[i] > angleRaw[i + 1] and angleRaw[i] < angle[-1]):
                    angle.append(angleRaw[i])
                    time.append(timeRaw[i])
                if (angleRaw[i] == angleRaw[i + 1]):
                    for j in range(i + 1, angleRaw.size):
                        if(angleRaw[i] < angleRaw[j]):
                            break
                        elif(angleRaw[i] > angleRaw[j]):
                            angle.append(angleRaw[j - 1])
                            avgTime = (timeRaw[i] + timeRaw[j - 1])/2.0
                            time.append(avgTime)
                            i = j
                            k = j - 1
                            break
                            
    prevAngle = angleRaw[k]
    # else:
    #     if(angleRaw[i] < angleRaw[i - 1]):
    #         if (angleRaw[i] < angleRaw[i + 1]):
    #             angle.append(angleRaw[i])
    #             time.append(timeRaw[i])
    #         elif (angleRaw[i] == angleRaw[i + 1]):
    #             for j in range(i + 1, angleRaw.size):
    #                 if(angleRaw[i] > angleRaw[j]):
    #                     break
    #                 elif(angleRaw[i] < angleRaw[j]):
    #                     angle.append(angleRaw[j])
    #                     avgTime = (timeRaw[i] + timeRaw[j])/2.0
    #                     time.append(avgTime)
    #                     i = j
    #                     break

time = np.array(time)
angle = np.array(angle)

# Set time error to be all 0.05s
time_error = np.full(shape=time.size, fill_value=0.05)

angle_error = np.full(shape=time.size, fill_value=np.deg2rad(0.3))

def exp_func(t, i0, tau, shift):
    return i0 * np.exp(-t/tau) + shift

fbb.plot_fit(exp_func, time, angle, xerror=time_error, yerror=angle_error, xlabel="Time (s)", ylabel="Angle (rad)", title="Amplitude vs Time")

# plt.plot(time, angle, 'bo', markersize = 1, label = 'data')

# popt, pcov = curve_fit(exp_func, time, angle)

# plt.plot(time, exp_func(time, *popt), 'r-', label = 'fit: i0=%5.3f, tau=%5.3f' % tuple(popt))

# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.show()