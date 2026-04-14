from flask import Flask, render_template, request, send_file
import os
from processing.utils import save_wav, read_wav
from processing.laplace import aplicar_laplace
from processing.edo import filtro_edo

app = Flask(__name__)
UPLOAD_FOLDER = 'audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    rate, data = read_wav(input_path)

    if metodo == 'laplace':
        filtered = aplicar_laplace(rate, data)
    else:
        filtered = filtro_edo(rate, data)

    save_wav(output_path, rate, filtered)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)