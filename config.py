import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:4753@localhost:3306/busdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings (cookies for web UI)
                