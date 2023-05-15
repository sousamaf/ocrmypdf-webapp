from flask import Flask, render_template, request, send_from_directory
import threading
import os
import ocrmypdf
from notifypy import Notify

app = Flask(__name__)

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
        filename = file.filename
        file.save(os.path.join("/app/uploads", filename))
        process_thread = threading.Thread(target=ocr_process, args=(filename,))
        process_thread.start()
        return 'File uploaded and processing started.'

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory("/app/uploads", filename)

def ocr_process(filename):
    input_file = os.path.join("/app/uploads", filename)
    output_file = os.path.join("/app/uploads", "output_" + filename)
    ocrmypdf.ocr(input_file, output_file)
    notify = Notify()
    notify.send('OCR processing finished. You can download your file.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
