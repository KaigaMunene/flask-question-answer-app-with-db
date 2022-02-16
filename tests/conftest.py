import pytest
import os
from app import app
from config import TestingConfig

from app.db import db


@pytest.fixture(scope="module")  # to run once for each testing instance
def flask_app():
    app.config.from_object(
        TestingConfig
    )  # acquires the configurations of testing from config.py
    db.create_tables()  # create the database and tables

    yield app  # like the return, everything before yield runs before the testing instance
    # and everything after yield runs after the testing instance

    os.remove(app.config["DB"])  # for deleting the database


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()
