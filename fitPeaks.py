from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

time_tare = 33.692

data = pd.read_csv("data31.csv", delimiter = ', ')
timeRaw = data['time'].to_numpy() - time_tare
angleRaw = data['angle'].to_numpy()

time = []
angle = []
prevAngle = 0
for i in range(0, angleRaw.size - 1):
    k = i
    if (prevAngle !=angleRaw[i - 1]):
        print(str(i) + " " + str(angleRaw[i - 1]) + " " + str(prevAngle))
    if(angleRaw[i] >= 0):
        if(angleRaw[i] > prevAngle):

            if (angleRaw[i] > angleRaw[i + 1]):
                angle.append(angleRaw[i])
                time.append(timeRaw[i])
            elif (angleRaw[i] == angleRaw[i + 1]):
                for j in range(i + 1, angleRaw.size):
                    if(angleRaw[i] < angleRaw[j]):
                        break
                    elif(angleRaw[i] > angleRaw[j]):
                        angle.append(angleRaw[j])
                        avgTime = (timeRaw[i] + timeRaw[j])/2.0
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

i_0 = 1.6441001553786583
p_0 = 0

def exp_func(t, tau):
    return i_0 * np.exp(-t/tau)

plt.plot(time, angle, 'bo', markersize = 1, label = 'data')

popt, pcov = curve_fit(exp_func, time, angle)

plt.plot(time, exp_func(time, *popt), 'r-', label = 'fit: tau=%5.3f, ' % tuple(popt))

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()