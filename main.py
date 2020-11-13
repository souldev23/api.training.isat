
from flask import Flask
from flask import app
from flask.globals import request
from flask.json import jsonify
from decouple import config as config_decouple
from cfg.config import config

def create_app(enviroment):
    print(enviroment)
    app = Flask(__name__)

    app.config.from_object(enviroment)

    return app

enviroment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(enviroment)

users = [{"user_name": "souldev", "name": "Saúl García", "mail": "soul23.4ever@gamil.com", "age":32, "active":True}]

@app.errorhandler(400)
def handle_400_error(e):
    resp={"ERR_CODE": 400, "ERR_DESC": "EL contenido del JSON tiene un error de formato", 
        "message":"Bad Request"}
    return jsonify(resp)

@app.route('/')
def hello():
    return "Hello."

@app.route('/v1/users/')
def getUsers():
    
    return jsonify({"users":users})

@app.route('/v1/user/<string:user_name>/uname')
def getUser(user_name):
    print(user_name)
    user = {}
    for us in users:
        print(us)
        if us["user_name"] == user_name:
            user = us
            break
    if user == {}:
        user = {"message":" No se ha encontrado el usuario en la base de datos"}
    return jsonify(user)

@app.route('/v1/users/', methods=['POST'])
def addUser():
    new_user = request.json
    print(new_user)
    users.append(new_user)
    resp={"ERR_CODE": 0, "ERR_DESC": "OK", "message":"El usuario se ha agregado correctamente"}
    return jsonify(resp)
    

@app.route('/v1/user/<string:user_name>/uname', methods=['PUT'])
def editUser(user_name):
    print(user_name)
    userFound = [us for us in users if us['user_name'] == user_name]
    print(userFound)
    if(len(userFound)>0):
        userFound[0]["user_name"] = request.json["user_name"]
        userFound[0]["name"] = request.json["name"]
        userFound[0]["mail"] = request.json["mail"]
        userFound[0]["age"] = request.json["age"]
        userFound[0]["active"] = request.json["active"]
        resp={"ERR_CODE": 0, "ERR_DESC": "OK", "message":"El usuario se ha actualizado correctamente"}
        return jsonify(resp)
    resp={"ERR_CODE": 0, "ERR_DESC": "OK", "message":"El usuario no se ha encontrado en la base de datos"}
    return jsonify(resp)
    

@app.route('/v1/user/<string:user_name>/uname', methods=["DELETE"])    
def deleteUser(user_name):
    print(user_name)
    userFound = [us for us in users if us["user_name"] == user_name]
    if(len(userFound) > 0):
        users.remove(userFound[0])
        resp={"ERR_CODE": 0, "ERR_DESC": "OK", "message":"El usuario se ha eliminado correctamente"}
        return jsonify(resp)
    resp={"ERR_CODE": 0, "ERR_DESC": "OK", "message":"El usuario no se ha encontrado en la base de datos"}
    return jsonify(resp)
    
    

