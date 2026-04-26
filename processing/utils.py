import os
import matplotlib
matplotlib.use('Agg')
import numpy as np
from scipy.signal import find_peaks
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

    Pxx, freqs, bins, im = plt.specgram(
        data,
        Fs=rate,
        scale='dB'
    )

    plt.title(titulo)
    plt.xlabel('Tiempo')
    plt.ylabel('Frecuencia')

    plt.savefig(path)
    plt.close()

def generar_grafica_comparacion(edo, euler, path):
    min_len = min(len(edo), len(euler))
    edo = np.nan_to_num(edo[:min_len])
    euler = np.nan_to_num(euler[:min_len])

    if np.max(np.abs(edo)) > 0:
        edo = edo / np.max(np.abs(edo))
    if np.max(np.abs(euler)) > 0:
        euler = euler / np.max(np.abs(euler))

    window_size = 50000
    x_env = []
    y_env = []

    for i in range(0, len(euler), window_size):
        segment = euler[i:i+window_size]
        if len(segment) == 0:
            continue
        peak_idx = np.argmax(segment)
        x_env.append(i + peak_idx)
        y_env.append(segment[peak_idx])

    step = max(1, len(edo) // 5000)
    x_plot = np.arange(len(edo))[::step]
    edo_plot = edo[::step]

    plt.figure(figsize=(10, 5))

    plt.plot(x_plot, edo_plot, color='blue', linewidth=1, label='Señal EDO')

    if len(x_env) > 0:
        plt.plot(x_env, y_env, color='orange', linewidth=2, label='Euler mejorado')

    plt.legend()
    plt.title('Comparación: EDO vs Euler Mejorado')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')

    plt.savefig(path)
    plt.close()