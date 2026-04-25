import os
import matplotlib
matplotlib.use('Agg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import librosa

def read_audio(path):
    # carga mp3 o wav directamente
    data, rate = librosa.load(path, sr=None, mono=True)

    # convertir a float32 (ya viene así normalmente)
    data = data.astype(np.float32)

    return rate, data

def save_wav(path, rate, data):
    if np.max(np.abs(data)) > 0:
        data = data / np.max(np.abs(data)) # normalizar a -6dB para evitar clipping
    data = (data * 32767).astype(np.int16)
    wavfile.write(path, rate, data)

def generar_grafica(data, path, titulo):
    plt.figure()
    plt.plot(data)
    plt.title(titulo)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.savefig(path)
    plt.close()
    
def generar_espectrograma(data, rate, path, titulo):
    plt.figure()

    plt.specgram(data, Fs=rate)
    plt.title(titulo)
    plt.xlabel('Tiempo')
    plt.ylabel('Frecuencia')

    plt.savefig(path)
    plt.close()