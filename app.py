from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"

@app.route("/")
def index():
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    projects = os.listdir(UPLOAD_FOLDER)
    return projects.__repr__() + "\n"


@app.route("/sounds/<path:path>")
def serve_static(path):
    return send_from_directory(UPLOAD_FOLDER, path)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["sound"]
    if file:
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        filename = uuid.uuid4().__str__() + ".wav" 
         
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)
