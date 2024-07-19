class Config:
    SECRET_KEY = 'HOLASSDASDASDASD'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'romario'
    MYSQL_PASSWORD = '1234567'
    MYSQL_DB = 'garage'

config = {
    'development': DevelopmentConfig
}
