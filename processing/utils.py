import os
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
    wavfile.write(path, rate, data.astype(np.int16))


def generar_grafica(data, path, titulo):
    plt.figure()
    plt.plot(data)
    plt.title(titulo)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.savefig(path)
    plt.close()
    
