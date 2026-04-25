import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, send_from_directory
from processing.utils import read_audio, save_wav, generar_grafica
from processing.edo import filtro_edo, filtro_euler_mejorado
# from processing.filters import filtro_voz
from processing.utils import generar_espectrograma

app = Flask(__name__)

UPLOAD_FOLDER = 'audio'
GRAPH_FOLDER = 'static/graphs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['audio']
    nivel_filtro = float(request.form.get('nivel_filtro', 5))

    #  limitar valores
    nivel_filtro = max(0.5, min(nivel_filtro, 10))

    #  guardar con extensión real
    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(UPLOAD_FOLDER, 'output.wav')

    file.save(input_path)

    #  leer audio (mp3 o wav)
    rate, data = read_audio(input_path)

    #  1. filtro de voz (frecuencias)
    # data_filtrada = filtro_voz(data, rate)

    #  2. EDO (Euler básico)
    filtered_edo = filtro_edo(rate, data, a=nivel_filtro)

    #  3. Euler mejorado (comparación)
    filtered_euler = filtro_euler_mejorado(rate, data, a=nivel_filtro)

    #  4. guardar salida
    save_wav(output_path, rate, filtered_edo)

    #  gráficas
    grafica_input = os.path.join(GRAPH_FOLDER, 'input.png')
    grafica_output = os.path.join(GRAPH_FOLDER, 'output.png')
    grafica_comparacion = os.path.join(GRAPH_FOLDER, 'comparacion.png')
    grafica_spec_input = os.path.join(GRAPH_FOLDER, 'spec_input.png')
    grafica_spec_output = os.path.join(GRAPH_FOLDER, 'spec_output.png')

    generar_espectrograma(data, rate, grafica_spec_input, 'Espectrograma Original')
    generar_espectrograma(filtered_edo, rate, grafica_spec_output, 'Espectrograma Filtrado')
    generar_grafica(data, grafica_input, 'Señal Original')
    generar_grafica(filtered_edo, grafica_output, 'Señal Filtrada (EDO)')
    generar_grafica_comparacion(filtered_edo, filtered_euler, grafica_comparacion)

    return render_template(
        'index.html',
        input_audio='input.wav',
        output_audio='output.wav',
        grafica_input='graphs/input.png',
        grafica_output='graphs/output.png',
        grafica_comparacion='graphs/comparacion.png',
        grafica_spec_input='graphs/spec_input.png',
        grafica_spec_output='graphs/spec_output.png'
    )


# función para comparar métodos
def generar_grafica_comparacion(edo, euler, path):
    plt.figure()
    plt.plot(edo, label='EDO (Euler básico)')
    plt.plot(euler, label='Euler mejorado', linestyle='--')
    plt.legend()
    plt.title('Comparación de Métodos')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')

    plt.savefig(path)
    plt.close()
    
    
@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory('audio', filename)

if __name__ == '__main__':
    app.run(debug=True)