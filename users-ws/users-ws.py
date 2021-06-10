import os
import json
 
from flask import Flask, request
 
app = Flask(__name__)
 
config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}

version_cfg = {"version": "2.4"}

@app.route("/")
def hello():
    return config['GREETING'] + ' from ' + config['HOSTNAME'] + '!'

@app.route("/config")
def configuration():
    return json.dumps(config)

@app.route("/health")
def health():
    return '{"status": "ok"}'

@app.route("/version", methods=['GET'])
def version():
    return json.dumps(version_cfg)

@app.route('/users/<user_id>', methods=['GET','DELETE','PUT'])
def get_user_by_id(user_id):
    from sqlalchemy import create_engine

    engine = create_engine(config['DATABASE_URI'], echo=True)
    if request.method == 'GET':
        rows = []
        with engine.connect() as connection:
            result = connection.execute("select id, name from client where id = %s;" % user_id)
            rows = [dict(r.items()) for r in result]
    
    if request.method == 'DELETE':
        with engine.connect() as connection:
            result = connection.execute("delete from client where id=%s;" % (user_id))
            rows = {"success": "True"}

    if request.method == 'PUT':
        request_data = request.get_json()

        user_name = request_data['name']
        user_age = request_data['age']

        with engine.connect() as connection:
            result = connection.execute("update client set name='%s', age=%s where id=%s;" % (user_name,user_age,user_id))
            rows = {"success": "True"}

    return json.dumps(rows), 201

@app.route('/users', methods=['POST'])
def post_user():
    request_data = request.get_json()

    user_id = request_data['id']
    user_name = request_data['name']
    user_age = request_data['age']

    from sqlalchemy import create_engine

    engine = create_engine(config['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = connection.execute("insert into client(id, name, age) values (%s,'%s',%s);" % (user_id,user_name,user_age))
    return json.dumps({"success": "True"}), 201

@app.route('/db')
def db():
    from sqlalchemy import create_engine

    engine = create_engine(config['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = connection.execute("select id, name, age from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
