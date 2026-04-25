import numpy as np
from scipy.signal import lti, lsim, butter, lfilter

# def filtro_voz(data, rate):
#     lowcut = 300.0
#     highcut = 3400.0

#     nyq = 0.5 * rate
#     low = lowcut / nyq
#     high = highcut / nyq

#     b, a = butter(4, [low, high], btype='band')
#     y = lfilter(b, a, data)

#     return y

def apply_lowpass_filter(rate, data, a=5):
    t = np.linspace(0, len(data)/rate, len(data))
    system = lti([1], [1, a])
    t, y, _ = lsim(system, data, t)
    return y