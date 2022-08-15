import os


class Config:
    SECRET_KEY = os.urandom(32)  # For initialize flask-wtforms
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRES_USERNAME')}:{os.environ.get('POSTGRES_PASSWORD')}@localhost:5432/flasky-dev"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRES_USERNAME')}:{os.environ.get('POSTGRES_PASSWORD')}@localhost:5432/flasky"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRES_USERNAME')}:{os.environ.get('POSTGRES_PASSWORD')}@localhost:5432/flasky-test"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
