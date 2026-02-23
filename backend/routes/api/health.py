from flask import jsonify
from routes.api import api_bp


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask-React Boilerplate backend is running'
    }), 200
