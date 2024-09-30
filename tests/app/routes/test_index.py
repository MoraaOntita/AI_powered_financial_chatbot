import pytest
from flask import json
from app import create_app  
from unittest.mock import patch

@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app()  # Ensure this creates the app with the proper configuration
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data  # Check for HTML content, adjust as necessary

def test_ask_question_success(client):
    """Test the ask_question route with valid input."""
    question = {"question": "What is the capital of France?"}
    
    # Mock the process_question function to return a specific answer
    with patch('app.services.chatbot.process_question', return_value="Paris"):
        response = client.post('/ask', json=question)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['question'] == question['question']
        assert data['answer'] == "Paris"

def test_ask_question_missing_key(client):
    """Test the ask_question route with missing 'question' key."""
    question = {}
    response = client.post('/ask', json=question)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Question is required'

def test_ask_question_invalid_data(client):
    """Test the ask_question route with invalid (non-JSON) data."""
    # Simulate a non-JSON data request (plain string, not a valid JSON format)
    response = client.post('/ask', data='invalid data', content_type='text/plain')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data  # Check for an error message indicating invalid content type

def test_ask_question_internal_error(client):
    """Test the ask_question route handling an internal error."""
    question = {"question": "What is the capital of France?"}
    
    # Mock the process_question function to raise an error
    with patch('app.services.chatbot.process_question', side_effect=Exception("Internal error")):
        response = client.post('/ask', json=question)
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['error'] == 'An error occurred while processing your request.'
