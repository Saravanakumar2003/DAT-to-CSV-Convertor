from flask import Flask, render_template, request, redirect, send_file, url_for
from conversion_utils import convert_dat_to_csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files/'
app.config['CONVERTED_FOLDER'] = 'converted_files/'

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        converted_filename = convert_dat_to_csv(file_path)
        if converted_filename:  # Check if the conversion was successful
            return redirect(url_for('download_file', filename=os.path.basename(converted_filename)))
        else:
            # Handle conversion failure or other errors
            return "Conversion failed. Please try again."

@app.route('/downloaded_files/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['CONVERTED_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
