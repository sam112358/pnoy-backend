from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    # Check if a file is in the request
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Save the file (you can also convert to PDF here if needed)
        filename = file.filename
        file.save(os.path.join(filename))
        return f'File {filename} uploaded successfully', 200

if __name__ == "__main__":
    app.run(debug=True)
