import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, send_from_directory
from processing.utils import read_audio, save_wav, generar_grafica, generar_espectrograma, generar_grafica_comparacion
from processing.edo import filtro_edo, filtro_euler_mejorado

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
    metodo = request.form.get('metodo')

    a_slider = float(request.form.get('a', 50))
    a_slider = max(0, min(a_slider, 100))
    a = 50 - (a_slider / 100) * 50

    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(UPLOAD_FOLDER, 'output.wav')

    file.save(input_path)

    rate, data = read_audio(input_path)

    filtered = filtro_edo(rate, data, a=a)
    filtered_euler = filtro_euler_mejorado(rate, data, a=a)

    save_wav(output_path, rate, filtered)

    grafica_input = os.path.join(GRAPH_FOLDER, 'input.png')
    grafica_output = os.path.join(GRAPH_FOLDER, 'output.png')
    grafica_comparacion = os.path.join(GRAPH_FOLDER, 'comparacion.png')
    grafica_spec_input = os.path.join(GRAPH_FOLDER, 'spec_input.png')
    grafica_spec_output = os.path.join(GRAPH_FOLDER, 'spec_output.png')

    generar_espectrograma(data, rate, grafica_spec_input, 'Espectrograma Original')
    generar_espectrograma(filtered, rate, grafica_spec_output, 'Espectrograma Filtrado')
    generar_grafica(data, grafica_input, 'Señal Original')
    generar_grafica(filtered, grafica_output, 'Señal Filtrada')

    generar_grafica_comparacion(filtered, filtered_euler, grafica_comparacion)

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

    
@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory('audio', filename)

if __name__ == '__main__':
    app.run(debug=True)