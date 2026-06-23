import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_page_has_content(client):
    response = client.get('/')
    assert b'System' in response.data

def test_response_is_html(client):
    response = client.get('/')
    assert b'<html>' in response.data or b'<!DOCTYPE' in response.data