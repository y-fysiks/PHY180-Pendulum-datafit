from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import readData as rd
import fit_black_box as fbb

def getPeriod(angleDeg, numOscillations, filename, tare, reverse = False):
    timeRaw, angleRaw = rd.readData(tare, filename, reverse)

    time = []
    angle = []
    measAngle = np.deg2rad(angleDeg)

    measure = False
    cntMeasure = 0
    periodStart = 0
    periodEnd = 0

    timeP = []
    angleP = []

    #measure the period for numOscillations following the peak closest to the specified angle
    prevAngle = 0
    for i in range(0, angleRaw.size - 1):
        k = i

        if(angleRaw[i] >= 0):
            if(angleRaw[i] > prevAngle):
                if (angleRaw[i] > angleRaw[i + 1]):
                    angle.append(angleRaw[i])
                    time.append(timeRaw[i])
                    # print(str(np.rad2deg(angleRaw[i])) + " " + str(time[-1]))

                    if (measure):
                        cntMeasure += 1
                        # print("cntMeasure: " + str(cntMeasure))

                    if (angle[-1] == measAngle):
                        measure = True
                        periodStart = time[-1]
                    
                    if angle[-1] < measAngle and angle[-2] > measAngle:
                        measure = True
                        if (measAngle - angle[-1]) < (angle[-2] - measAngle):
                            periodStart = time[-1]
                        else:
                            periodStart = time[-2]
                            timeP.append(time[-2])
                            angleP.append(angle[-2])
                        
                elif (angleRaw[i] == angleRaw[i + 1]):
                    for j in range(i + 1, angleRaw.size):
                        if(angleRaw[i] < angleRaw[j]):
                            i = j - 1
                            break
                        elif(angleRaw[i] > angleRaw[j]):
                            angle.append(angleRaw[j - 1])
                            avgTime = (timeRaw[i] + timeRaw[j - 1])/2.0
                            time.append(avgTime)
                            i = j
                            k = j - 1

                            # print(str(np.rad2deg(angleRaw[j])) + " " + str(avgTime))

                            if (measure):
                                cntMeasure += 1
                                # print("cntMeasure: " + str(cntMeasure))

                            if (angle[-1] == measAngle):
                                measure = True
                                periodStart = time[-1]
                            
                            if angle[-1] < measAngle and angle[-2] > measAngle:
                                measure = True
                                if (measAngle - angle[-1]) < (angle[-2] - measAngle):
                                    periodStart = time[-1]
                                else:
                                    periodStart = time[-2]
                                    timeP.append(time[-2])
                                    angleP.append(angle[-2])
                                    cntMeasure = 1
                            break
        if(cntMeasure == numOscillations):
            periodEnd = time[-1]
            break
        if (measure):
            timeP.append(timeRaw[i])
            angleP.append(angleRaw[i])

        prevAngle = angleRaw[k]

    period = (periodEnd - periodStart) / numOscillations
    # print("period: " + str(period))
    # print("angle: " + str(np.rad2deg(angleP[0])))

    return [angleP[0], period]

angles = []
periods = []
angleUncerts = []
periodUncerts = []

for i in range(23, 5-1, -2):
    angle1, period1 = getPeriod(i, 3, "data31.csv", 33.692)
    angle2, period2 = getPeriod(i, 3, "data32.csv", 10.14)
    angle3, period3 = getPeriod(i, 3, "data33.csv", 9.487)

    maxError = max(abs(angle1 - np.deg2rad(i)), abs(angle2 - np.deg2rad(i)), abs(angle3 - np.deg2rad(i)))
    angleUncerts.append(maxError + np.deg2rad(0.15))
    periodUncerts.append(0.005)

    angle = np.deg2rad(i)
    period = (period1 + period2 + period3) / 3.0
    angles.append(angle)
    periods.append(period)
    print("angle: " + str(i) + " period: " + str(periods[-1]))
    print("angle1: " + str(np.rad2deg(angle1)) + " angle2: " + str(np.rad2deg(angle2)) + " angle3: " + str(np.rad2deg(angle3)))
    print("Error: " + str(np.rad2deg(maxError)) + "; +-" + str(np.rad2deg(angleUncerts[-1])) + " deg")


for i in range(5, 23+1, 2):
    angle1, period1 = getPeriod(i, 3, "data31.csv", 33.692, True)
    angle2, period2 = getPeriod(i, 3, "data32.csv", 10.14, True)
    angle3, period3 = getPeriod(i, 3, "data33.csv", 9.487, True)


    maxError = max(abs(angle1 - np.deg2rad(i)), abs(angle2 - np.deg2rad(i)), abs(angle3 - np.deg2rad(i)))
    angleUncerts.append(maxError + np.deg2rad(0.15))
    periodUncerts.append(0.005)

    angle = np.deg2rad(-i)
    period = (period1 + period2 + period3) / 3.0
    angles.append(angle)
    periods.append(period)
    print("angle: " + str(i) + " period: " + str(periods[-1]))
    print("angle1: " + str(np.rad2deg(angle1)) + " angle2: " + str(np.rad2deg(angle2)) + " angle3: " + str(np.rad2deg(angle3)))
    print("Error: " + str(np.rad2deg(maxError)) + "; +-" + str(np.rad2deg(angleUncerts[-1])) + " deg")

angles = np.array(angles)
periods = np.array(periods)

def power_series(x, T0, B, C):
    return (T0 * (1.0 + B * x + C * (x ** 2)))

fbb.plot_fit(power_series, angles, periods, xerror=angleUncerts, yerror=periodUncerts, xlabel="Angle (rad)", ylabel="Period (s)", title = "Period vs Angle of Pendulum")

anglesPlot = np.array([np.deg2rad(x) for x in range(-80, 80+1, 1)])

