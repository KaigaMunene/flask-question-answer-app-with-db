import sqlite3
from flask import Flask

app = Flask(__name__)


def get_connection():
    connection = None
    try:
        connection = sqlite3.connect("flask_database.db")

    except Exception as e:
        print(e)
    
    return connection
    
from app import routes
