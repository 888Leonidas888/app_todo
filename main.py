from flask import Flask
from flask import jsonify, request
from flask_cors import CORS
from os import getenv
from conecction import DBStorage

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route('/read_all', strict_slashes=False, methods=['GET'])
def read_all():
    cnn = DBStorage('root', getenv('mysql_pass'), 'todo_db')
    cnn.connect()
    records = cnn.read()

    if records:
        return jsonify({'data': records})
    else:
        return jsonify({'data': False})


@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    id = data['id']
    cnn = DBStorage('root', getenv('mysql_pass'), 'todo_db')
    cnn.connect()
    results = cnn.delete(id)

    if results:
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})


@app.route('/update', strict_slashes=False, methods=['POST'])
def update():
    data = request.get_json()
    id = data.get('id', None)

    if id is None:
        print('id no encontrado')
        return False

    title = data.get('title', None)
    description = data.get('description', None)
    status = data.get('status', None)

    cnn = DBStorage('root', getenv('mysql_pass'), 'todo_db')
    cnn.connect()
    results = (cnn.update(id, title, description, status))

    if results:
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})


@app.route('/create', strict_slashes=False, methods=['POST'])
def create():
    data = request.get_json()

    title = data.get('title', 'sin titulo')
    description = data.get('description', 'sin descripcion')
    status = data.get('status', False)

    cnn = DBStorage('root', getenv('mysql_pass'), 'todo_db')
    cnn.connect()
    results = (cnn.create(title, description, status))

    if results:
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})


if __name__ == '__main__':
    app.run(debug=True)
