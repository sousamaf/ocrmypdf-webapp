from flask import Flask, render_template, request, send_from_directory
import threading
import os
import sys
import ocrmypdf
from notifypy import Notify
import re
from flask import jsonify
from unidecode import unidecode

app = Flask(__name__)

# UPLOAD_FOLDER = '/app/uploads'
UPLOAD_FOLDER = '/home/marco/Documents/git/ocrmypdf-webapp/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def format_filename(filename):
    # Remove a extensão do arquivo (supõe-se que seja .pdf)
    filename = filename.rsplit('.', 1)[0]
    # Substitui caracteres especiais por seus equivalentes
    filename = unidecode(filename)
    # Substitui espaços e outros caracteres não alfanuméricos por "-"
    filename = re.sub(r'\W+', '-', filename)
    # Adiciona a extensão .pdf de volta
    filename = filename + ".pdf"
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        original_filename = file.filename
        filename = format_filename(original_filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        process_thread = threading.Thread(target=ocr_process, args=(filename,))
        process_thread.start()
        messages = [{'title': 'Processamento!',
             'content': 'Arquivo recebido e em processamento. Você receberá uma notificação no Windows quando o arquivo estiver pronto.'},
            ]
        return render_template('index.html', messages=messages)


@app.route('/recent_files', methods=['GET'])
def get_recent_files():
    directory = app.config['UPLOAD_FOLDER']
    files = os.listdir(directory)
    files = [file for file in files if file.startswith('ocr_') and file.endswith('.pdf')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    recent_files = files[:5]
    print(files, file=sys.stderr)

    ## Remove os arquivos mais antigos
    
    remove_files = files[10:]
    for file in remove_files:
        os.remove(os.path.join(directory, file))
        original = file.replace('ocr_', '', 1)
        os.remove(os.path.join(directory, original))

    return jsonify(recent_files)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def ocr_process(filename):
    input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], "ocr_" + filename)
    ocrmypdf.ocr(
        input_file, 
        output_file, 
        rotate_pages=True,
        deskew=True, 
        force_ocr=True, 
        tesseract_oem=2, 
        jobs=3,
        output_type='pdfa',
        lang='por'
    )

    # ocrmypdf.ocr(input_file, output_file)
    notify = Notify()
    notify.send('OCR processamento concluído. Você pode baixar o arquivo.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
