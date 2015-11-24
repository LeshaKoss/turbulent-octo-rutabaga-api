from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"

@app.route("/")
def index():
    return send_from_directory('static/', 'index.html')
    
@app.route("/<path:path>")
def index():
    return send_from_directory('static/', path)

@app.route("/sounds")
def get_sounds_list():
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    sounds = os.listdir(UPLOAD_FOLDER)
    return jsonify({'sounds': sounds})


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
        return filename + "\n"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)
