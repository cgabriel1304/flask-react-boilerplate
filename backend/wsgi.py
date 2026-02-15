"""WSGI entry point for production deployment"""
import os
from app import create_app
from db import db

app = create_app(os.getenv('FLASK_ENV', 'production'))


@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell"""
    return {'db': db}


if __name__ == '__main__':
    app.run()
