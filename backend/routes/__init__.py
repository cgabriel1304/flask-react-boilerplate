from routes.api import api_bp
from routes.static import static_bp


def register_routes(app):
    """Register all blueprints on the Flask app."""
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(static_bp)
