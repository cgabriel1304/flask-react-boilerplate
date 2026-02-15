import logging
import os

from flask import Flask
from config import config


def create_app(config_name=None):
    """Application factory function"""

    # Get environment or use default
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # Create Flask app with public folder for static files
    app = Flask(__name__, static_folder='public', static_url_path='')

    # Configure logging
    log_level = logging.DEBUG if app.debug or config_name == 'development' else logging.INFO
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        level=log_level,
    )

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    from db import db
    db.init_app(app)

    # Register all routes
    from routes import register_routes
    register_routes(app)

    # Create tables with app context
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
