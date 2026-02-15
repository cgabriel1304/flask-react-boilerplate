from flask import jsonify
from routes.api import api_bp


@api_bp.route('/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    return jsonify({'status': 'API is running'}), 200
