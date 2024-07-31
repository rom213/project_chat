from .users import users_bp
from .vehicles import vehicles_bp
from .casa import home_bp
from .sokets import sokets_bp, register_socketio_events

def init_app(app, socketio):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(sokets_bp, url_prefix='/socket')
    app.register_blueprint(home_bp, url_prefix='/')
    socketio.init_app(app)