import logging

from flask import Blueprint, jsonify, send_from_directory, current_app, request
from db import db

logger = logging.getLogger(__name__)

static_bp = Blueprint('static', __name__)


@static_bp.before_request
def log_static_request():
    logger.debug('%s %s', request.method, request.path)


@static_bp.route('/')
def index():
    """Serve frontend index.html"""
    return send_from_directory(current_app.static_folder, 'index.html')


@static_bp.app_errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404


@static_bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500
