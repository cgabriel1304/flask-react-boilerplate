"""Tests for API blueprint routes."""
from flask import Flask
from routes import api_bp


class TestApiBlueprintRegistration:
    def test_blueprint_has_api_prefix(self):
        assert api_bp.url_prefix == '/api'

    def test_blueprint_registers_on_app(self):
        app = Flask(__name__)
        app.register_blueprint(api_bp)
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert '/api/status' in rules


class TestApiStatus:
    def setup_method(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp)
        self.client = self.app.test_client()

    def test_status_returns_200(self):
        response = self.client.get('/api/status')
        assert response.status_code == 200

    def test_status_returns_running(self):
        response = self.client.get('/api/status')
        data = response.get_json()
        assert data['status'] == 'API is running'
