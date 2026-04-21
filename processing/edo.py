import numpy as np


def filtro_edo(rate, data, a=10):
    dt = 1 / rate
    y = np.zeros(len(data))

    for i in range(1, len(data)):
        dy = data[i] - a * y[i-1]
        y[i] = y[i-1] + dt * dy

    return y