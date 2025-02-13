from flask import Flask, render_template, request, redirect, send_file, url_for
from conversion_utils import convert_dat_to_csv
import os
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files/'
app.config['CONVERTED_FOLDER'] = 'converted_files/'

# Define the desired order of fieldnames
fieldnames_order = [
    "Timestamp", "ALT200_SPEED", "ALT190_SPEED", "ALT180_SPEED", "ALT170_SPEED", "ALT160_SPEED", "ALT150_SPEED", "ALT140_SPEED", "ALT130_SPEED", "ALT120_SPEED", "ALT110_SPEED", "ALT100_SPEED", "ALT90_SPEED", "ALT80_SPEED", "ALT70_SPEED", "ALT60_SPEED", "ALT50_SPEED", "ALT40_SPEED", "ALT30_SPEED", "ALT200_DIR", "ALT190_DIR", "ALT180_DIR", "ALT170_DIR", "ALT160_DIR", "ALT150_DIR", "ALT140_DIR", "ALT130_DIR", "ALT120_DIR", "ALT110_DIR", "ALT100_DIR", "ALT90_DIR", "ALT80_DIR", "ALT70_DIR", "ALT60_DIR", "ALT50_DIR", "ALT40_DIR", "ALT30_DIR"
]

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("files[]")
    output_rows = []

    for file in uploaded_files:
        if file.filename == '':
            continue

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        converted_data = convert_dat_to_csv(file_path)
        output_rows.extend(converted_data)

    output_rows = [row for row in output_rows if isinstance(row, dict)]

    if output_rows:
        output_file_path = os.path.join(app.config['CONVERTED_FOLDER'], 'output.csv')

        fieldnames = set()
        for row in output_rows:
            fieldnames.update(row.keys())

        ordered_fieldnames = [fieldname for fieldname in fieldnames_order if fieldname in fieldnames]
        remaining_fieldnames = [fieldname for fieldname in fieldnames if fieldname not in ordered_fieldnames]
        ordered_fieldnames.extend(remaining_fieldnames)

        with open(output_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=ordered_fieldnames, restval="N/A")
            writer.writeheader()
            writer.writerows(output_rows)

        return redirect(url_for('download_file', filename='output.csv'))
    else:
        return "Conversion failed. Please try again."

@app.route('/downloaded_files/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['CONVERTED_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)