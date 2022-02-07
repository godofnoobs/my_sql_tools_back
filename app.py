import os.path
import logging
from flask import Flask, make_response, request
from flask_cors import CORS
import json
from utils.roll_up_history import get_roll_up_query

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        static_folder = 'static'
        src = os.path.join(root_dir(), static_folder, filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

app = Flask(__name__, static_folder="static_dir")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/roll_up", methods = ['GET'])
def api_roll_up():
    params = json.loads(request.args.get('txt').replace("'", '"'))
    print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ1', params)
    query_text = get_roll_up_query(**params)
    print(query_text)
    res_obj = {'query_text':query_text}
    res = make_response(
        res_obj
    )
    return res

@app.route('/<path:path>')
def get_resource(path):
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(path)
    res = make_response(
        content
    )
    res.mimetype = mimetype
    return res

@app.route('/', methods=['GET'])
def serve_static():
    content = get_file('index.html')
    return  make_response(
        content
    )

    
if __name__ == '__main__':
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True)
