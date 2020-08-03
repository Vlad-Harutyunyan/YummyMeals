class Config:
    SECRET_KEY = "not_secret_key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'yummymealbook@gmail.com'
    MAIL_PASSWORD = '789456123yummy'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True