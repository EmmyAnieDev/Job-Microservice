import pytest
from flask import Flask
from app.api.db import db
from flask_marshmallow import Marshmallow

@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma = Marshmallow(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def app_context(app):
    """Provide Flask application context for tests"""
    with app.app_context():
        yield