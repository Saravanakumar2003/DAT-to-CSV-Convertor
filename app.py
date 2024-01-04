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
def upload_form(): # This function is called when the user visits the homepage
    return render_template('upload.html') # This function returns the upload.html template

@app.route('/', methods=['POST'])
def upload_files(): 
    uploaded_files = request.files.getlist("files[]") # Get the uploaded files from the request
    output_rows = [] # This list will contain the converted data from the uploaded files

    for file in uploaded_files: # Iterate through the uploaded files
        if file.filename == '': # If the user did not select a file, skip it
            continue 

        filename = file.filename # Get the filename of the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Create the path to save the file to
        file.save(file_path) # Save the file to the path

        converted_data = convert_dat_to_csv(file_path) # Convert the file to a list of dictionaries
        output_rows.extend(converted_data) # Add the converted data to the output_rows list

    # Filter out non-dictionary objects from output_rows
    output_rows = [row for row in output_rows if isinstance(row, dict)]

    if output_rows:
        output_file_path = os.path.join(app.config['CONVERTED_FOLDER'], 'output.csv')

        # Derive fieldnames from the keys of dictionaries in output_rows
        fieldnames = set()
        for row in output_rows:
            fieldnames.update(row.keys())

        # Order the fieldnames according to the specified order
        ordered_fieldnames = [fieldname for fieldname in fieldnames_order if fieldname in fieldnames]
        remaining_fieldnames = [fieldname for fieldname in fieldnames if fieldname not in ordered_fieldnames]
        ordered_fieldnames.extend(remaining_fieldnames)

        # Write the output_rows to a CSV file
        with open(output_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=ordered_fieldnames, restval="N/A")
            writer.writeheader()
            writer.writerows(output_rows)

        # Return the output file to the user
        return redirect(url_for('download_file', filename='output.csv'))
    else:
        return "Conversion failed. Please try again."

@app.route('/downloaded_files/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['CONVERTED_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return str(e)
# Run the app
if __name__ == "__main__":
    app.run(debug=True)
