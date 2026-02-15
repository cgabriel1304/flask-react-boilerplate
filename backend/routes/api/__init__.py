import logging

from flask import Blueprint, request

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


@api_bp.before_request
def log_api_request():
    logger.info('%s %s', request.method, request.path)


from routes.api import health, status  # noqa: E402, F401
