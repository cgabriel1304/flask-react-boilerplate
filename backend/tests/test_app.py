"""Tests for application factory and core routes."""


class TestCreateApp:
    def test_app_is_created(self, app):
        assert app is not None

    def test_testing_config_applied(self, app):
        assert app.config['TESTING'] is True

    def test_static_folder_is_public(self, app):
        assert app.static_folder.endswith('public')


class TestHealthCheck:
    def test_health_returns_200(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_health_returns_message(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert 'message' in data


class TestErrorHandlers:
    def test_404_returns_json(self, client):
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Not found'

    def test_404_includes_message(self, client):
        response = client.get('/nonexistent-route')
        data = response.get_json()
        assert 'message' in data
