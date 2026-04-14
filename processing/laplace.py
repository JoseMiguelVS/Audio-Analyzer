import numpy as np
from scipy.signal import lti, lsim


def sistema_laplace(a=5):
    return lti([1], [1, a])


def aplicar_laplace(rate, data, a=5):
    t = np.linspace(0, len(data)/rate, len(data))
    system = sistema_laplace(a)
    t, y, _ = lsim(system, data, t)
    return y