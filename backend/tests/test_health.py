class TestHealthCheck:
    def test_health_returns_200(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_returns_correct_json(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['message'] == 'Cyberitance backend is running'
