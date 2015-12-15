from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import shutil
import psycopg2
import urlparse
import json
from psycopg2.extras import Json

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
db = conn.cursor()
psycopg2.extensions.register_adapter(dict, Json)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"

@app.route("/")
def index():
    return send_from_directory('static/', 'index.html')

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory('static/', path)

@app.route("/sounds")
def get_sounds_list():
    db.execute("""SELECT * FROM files""")
    rows = db.fetchall()
    _sounds = []
    for row in rows:
        _sounds.append(row[0])
    return jsonify({'sounds': _sounds})


@app.route("/sounds/<path:path>")
def serve_static(path):
    return send_from_directory(UPLOAD_FOLDER, path)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    info = json.JSONDecoder().decode(request.values["info"])

    if file:
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        filename = uuid.uuid4().__str__()

        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_desc = {"filename": info['filename'], "title": info['title']}
        db.execute("INSERT INTO files VALUES(%s)", [file_desc])
        conn.commit()
        return filename + "\n"

@app.route("/del")
def delete():
    try:
        shutil.rmtree(UPLOAD_FOLDER)
        db.execute("""DELETE FROM files""")
        conn.commit()
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': str(e)})


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)
