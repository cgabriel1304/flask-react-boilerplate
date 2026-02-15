# Backend API Routes
# Add your API blueprints here

from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')


# Import routes
# from . import user_routes
# from . import health_routes

# Register routes
# api_bp.register_blueprint(user_routes.bp)


@api_bp.route('/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    from flask import jsonify
    return jsonify({'status': 'API is running'}), 200
