import pandas as pd
import numpy as np

def readData(time_tare, filename, reverse = False):
    data = pd.read_csv(filename, delimiter = ', ', engine='python')
    time = data['time'].to_numpy() - time_tare
    if not reverse:
        angle = data['angle'].to_numpy()
    else:
        angle = [-x for x in data['angle']]
        angle = np.array(angle)
    return [time, angle]

def readData(filename, reverse = False):
    data = pd.read_csv(filename, delimiter = ', ', engine='python')
    time = data['timestamp'].to_numpy() - data['timestamp'][0]
    if not reverse:
        angle = data['angle'].to_numpy()
    else:
        angle = [-x for x in data['angle']]
        angle = np.array(angle)
    return [time, angle]