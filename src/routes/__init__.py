from .users import users_bp
from .vehicles import vehicles_bp
from .casa import home_bp


def init_app(app):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(home_bp, url_prefix='/')
  
