from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import fit_black_box as fbb
import dataAnalyze
import readData

def linear_func(x, m, b):
    return m * x + b

def quadratic_func(x, a, b, c):
    return np.multiply(a, np.power(x, 2)) + np.multiply(b, x) + c

def exp_func(t, i0, tau):
    return i0 * np.exp(-t/tau)

def pow(x, k, n):
    return np.multiply(k, np.power(x, n))

files = ["data2_10.csv", "data2_14.csv", "data2_15.csv", "data2_16.csv", "data2_17.csv", "data2_19.csv", "data2_20.csv", "data2_21.csv", "data2_25.csv", "data2_27.csv", "data2_29.csv"]

qFactors = []
uncertQF = []
lengths = []
uncertLength = []

periods = []
uncertPeriod = []

for i in range(0, len(files)):
    times, angles = readData.readData("Lab2/" + files[i])
    endSkip = angles[-1]
    angles = angles - endSkip

    angleError = np.full(shape=times.size, fill_value=(abs(endSkip) + 0.15/2))

    timePeaks, anglePeaks = dataAnalyze.getPeaks(times, angles, np.deg2rad(20))

    avgP = 0
    for j in range(len(timePeaks) - 1):
        if anglePeaks[j] < np.deg2rad(2.5):
            break
        # find period
        avgP += timePeaks[j + 1] - timePeaks[j]
    avgP /= len(timePeaks) - 1

    # plt.plot(timePeaks, anglePeaks, 'bo', markersize = 1, label = 'data')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.show()


    popt, pcov = curve_fit(exp_func, timePeaks, anglePeaks)

    print(popt)
    # print(pcov)

    # Q = np.pi * popt[1] / avgP


    target = anglePeaks[0] * np.exp(-np.pi/4)
    print(anglePeaks[0])
    Q = 0
    for j in range(0, len(anglePeaks)):
        if (anglePeaks[j] < target):
            Q = j - 0.5
            break
    Q *= 4

    qFactors.append(Q)
    lengths.append((527.01 - (i * 40)) / 1000)
    uncertQF.append(1)
    uncertLength.append(0.05 / 1000)
    periods.append(avgP)
    uncertPeriod.append(0.0000000005)

fbb.plot_fit(quadratic_func, lengths, qFactors, xerror=uncertLength, yerror=uncertQF, xlabel="Length(mm)", ylabel="Q Factor", title="Q Factor Dependency on Length")

fbb.plot_fit(pow, lengths, periods, xerror=uncertLength, yerror=uncertPeriod, xlabel="Length(mm)", ylabel="Period", title="Period Dependency on Length")
