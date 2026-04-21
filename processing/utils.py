import os
import matplotlib
matplotlib.use('Agg')

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def read_audio(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".wav":
        rate, data = wavfile.read(path)
    else:
        audio = AudioSegment.from_file(path)
        temp_path = "audio/temp.wav"
        audio.export(temp_path, format="wav")
        rate, data = wavfile.read(temp_path)

    data = data.astype(np.float32)

    # 🔥 CONVERTIR A MONO SI ES ESTÉREO
    if len(data.shape) == 2:
        data = np.mean(data, axis=1)

    return rate, data


def save_wav(path, rate, data):
    # 🔥 evitar división por cero
    if np.max(np.abs(data)) > 0:
        data = data / np.max(np.abs(data))

    # 🔥 escalar a int16
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
    
