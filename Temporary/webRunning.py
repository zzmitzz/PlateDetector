import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def process_image_or_video(file):
    # Your custom image/video processing code goes here
    # Replace the following with your actual processing code
    return cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if file:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process the image/video
            processed_image = process_image_or_video(cv2.imread(file_path))

            # Save the processed image
            processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + file.filename)
            cv2.imwrite(processed_file_path, processed_image)

            return render_template('index.html', processed_image=processed_file_path)

    return render_template('index.html', processed_image=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
