import os
import matplotlib
matplotlib.use('Agg')
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def read_audio(path):
    ext = os.path.splitext(path)[1].lower()

    # 🔥 Cargar audio (wav o mp3)
    if ext == ".wav":
        rate, data = wavfile.read(path)
    else:
        audio = AudioSegment.from_file(path)

        # Convertir a WAV temporal
        temp_path = "audio/temp.wav"
        audio.export(temp_path, format="wav")

        rate, data = wavfile.read(temp_path)

    # Convertir a float
    data = data.astype(np.float32)

    # 🔥 Convertir a mono (MUY IMPORTANTE)
    if len(data.shape) > 1:
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
    
