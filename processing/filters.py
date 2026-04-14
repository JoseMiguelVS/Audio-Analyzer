import numpy as np
from scipy.signal import lti, lsim

# Filtro basado en Laplace: H(s) = 1 / (s + a)
def apply_lowpass_filter(rate, data, a=5):
    t = np.linspace(0, len(data)/rate, len(data))
    system = lti([1], [1, a])
    t, y, _ = lsim(system, data, t)
    return y