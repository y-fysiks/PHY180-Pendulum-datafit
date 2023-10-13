import numpy as np

def getPeaks(timeRaw, angleRaw, cutoff):
    time = []
    angle = []
    prevAngle = 0
    for i in range(1, angleRaw.size - 1):
        k = i
        if(angleRaw[i] >= 0):
            if(angleRaw[i] > angleRaw[i - 1]):

                if (angleRaw[i] > angleRaw[i + 1]):
                    angle.append(angleRaw[i])
                    time.append(timeRaw[i])
                # elif (angleRaw[i] == angleRaw[i + 1]):
                #     for j in range(i + 1, angleRaw.size):
                #         if(angleRaw[i] < angleRaw[j]):
                #             break
                #         elif(angleRaw[i] > angleRaw[j]):
                #             angle.append(angleRaw[j - 1])
                #             avgTime = (timeRaw[i] + timeRaw[j - 1])/2.0
                #             time.append(avgTime)
                #             i = j
                #             k = j - 1
                #             break
        prevAngle = angleRaw[k]
    tare = 0
    for i in range(len(angle) - 1, -1, -1):
        if (angle[i] > cutoff):
            tare = time[i + 1]
            for j in range(i, -1, -1):
                angle = np.delete(angle, 0)
                time = np.delete(time, 0)

            break
    time = np.array(time) - tare
    return time, angle
    

