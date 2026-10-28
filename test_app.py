import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_home_get_route(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Student Grade Calculator" in data['application']

def test_marks_calculation_push2(client):
    payload = {"marks": list((80, 70, 90))}
    response = client.post('/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 240
    assert data['average'] == 80.0
    assert data['grade'] == 'B'
    assert "using Push 2 logic!" in data['message']

def test_invalid_payload(client):
    payload = {"invalid_key": list((10, 20))}
    response = client.post('/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
