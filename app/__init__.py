import sqlite3
from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)


def get_connection():
    connection = None
    try:
        connection = sqlite3.connect(app.config["DB"])

    except Exception as e:
        print(e)

    return connection


from app import routes
