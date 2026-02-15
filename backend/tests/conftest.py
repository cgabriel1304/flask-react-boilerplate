"""Pytest configuration"""
import pytest
import os
from app import create_app, db as _db


@pytest.fixture(scope='session')
def app():
    """Create application for tests"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def db(app):
    """Create database for tests"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
