from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import fit_black_box as fbb

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
                        angle.append(angleRaw[j - 1])
                        avgTime = (timeRaw[i] + timeRaw[j - 1])/2.0
                        time.append(avgTime)
                        i = j
                        k = j - 1
                        break
    prevAngle = angleRaw[k]

cutoff = np.deg2rad(21)
for i in range(len(angle) - 1, -1, -1):
    if (angle[i] > cutoff):
        for j in range(i, -1, -1):
            angle = np.delete(angle, 0)
            time = np.delete(time, 0)

        break

target = angle[0] * np.exp(-np.pi/2)
Q = 0
for i in range(0, len(angle)):
    if (angle[i] < target):
        Q = i - 0.5
        break
Q = 2 * Q
print(Q)