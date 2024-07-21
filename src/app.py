from flask import Flask, render_template
from flask_socketio import SocketIO, send
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import LoginManager
from models.ModelUser import ModelUser
from routes import init_app as init_routes

app = Flask(__name__)
app.config.from_object(config['development'])

db = SQLAlchemy(app)
mysql = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)


socketIO = SocketIO(app, cors_allowed_origins="*")


@socketIO.on('message')
def handle_message(message):
    print("received message= " + message)
    if message != "User connected!":
        send(message, broadcast=True)


@app.route('/')
def index():
    return render_template("index.html")


init_routes(app)

if __name__ == '__main__':
    socketIO.run(app, host='localhost', port=5001, debug=True)

