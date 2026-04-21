from flask import Flask, render_template, request
import os
from processing.utils import save_wav, read_audio, generar_grafica
from processing.laplace import aplicar_laplace
from processing.edo import filtro_edo

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

    input_path = os.path.join(UPLOAD_FOLDER, 'input.wav')
    output_path = os.path.join(UPLOAD_FOLDER, 'output.wav')

    file.save(input_path)

    rate, data = read_audio(input_path)

    if metodo == 'laplace':
        filtered = aplicar_laplace(rate, data)
    else:
        filtered = filtro_edo(rate, data)

    save_wav(output_path, rate, filtered)

    # Generar gráficas
    grafica_input = os.path.join(GRAPH_FOLDER, 'input.png')
    grafica_output = os.path.join(GRAPH_FOLDER, 'output.png')

    generar_grafica(data, grafica_input, 'Señal Original')
    generar_grafica(filtered, grafica_output, 'Señal Filtrada')

    return render_template('index.html',
                           input_audio=input_path,
                           output_audio=output_path,
                           grafica_input=grafica_input,
                           grafica_output=grafica_output)

if __name__ == '__main__':
    app.run(debug=True)