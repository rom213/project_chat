class DevelopmentConfig:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://romario:1234567@localhost:3306/garage'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'src/uploads/'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'romario'
    MYSQL_PASSWORD = '1234567'
    MYSQL_DB = 'garage'

config = {
    'development': DevelopmentConfig
}
