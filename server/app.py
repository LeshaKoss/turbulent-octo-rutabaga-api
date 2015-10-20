from flask import Flask, request
from werkzeug import secure_filename
import os
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/upload", methods=['POST'])
def upload_file():
    file = request.files['sound']
    print file.filename
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename

if __name__ == "__main__":
    app.run(debug=True)
