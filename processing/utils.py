import numpy as np
from scipy.io import wavfile


def read_wav(path):
    rate, data = wavfile.read(path)
    return rate, data.astype(np.float32)


def save_wav(path, rate, data):
    wavfile.write(path, rate, data.astype(np.int16))
