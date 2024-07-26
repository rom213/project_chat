from flask import Flask, render_template
from flask_socketio import SocketIO, send
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import LoginManager
from models.ModelUser import ModelUser
from routes import init_app, register_socketio_events

app = Flask(__name__)
app.config.from_object(config['development'])

db = SQLAlchemy(app)
mysql = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)

socketIO = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template("index.html")

init_app(app, socketIO)
register_socketio_events(socketIO)

if __name__ == '__main__':
    socketIO.run(app, host='0.0.0.0', port=5000, debug=True)
