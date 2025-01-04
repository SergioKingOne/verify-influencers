import pytest
from unittest.mock import Mock, patch
from flask import Flask
from app.services.claim_extraction_service import (
    ClaimExtractionService,
    HealthClaimsResponse,
)


@pytest.fixture
def app():
    """Create a Flask app for testing"""
    app = Flask(__name__)
    return app


@pytest.fixture
def mock_app_context(app):
    """Mock Flask app context with logger"""
    mock_logger = Mock()
    app.logger = mock_logger
    with app.app_context():
        with patch("flask.current_app.logger", mock_logger):
            yield mock_logger


@pytest.fixture
def service(mock_app_context):
    """Create ClaimExtractionService instance with mocked dependencies"""
    return ClaimExtractionService()


@pytest.fixture
def mock_ollama_response():
    """Mock successful ollama response"""
    return {
        "message": {
            "content": """
            {
                "claims": [
                    {
                        "text": "Exercise reduces heart disease risk",
                        "confidence": 0.9
                    },
                    {
                        "text": "Running improves mood",
                        "confidence": 0.6
                    }
                ]
            }
            """
        }
    }


def test_extract_health_claims_successful(app, service, mock_ollama_response):
    """Test successful extraction of health claims"""
    tweets = ["Exercise daily reduces heart disease risk by 30%"]

    with app.app_context():
        with patch("ollama.chat", return_value=mock_ollama_response):
            results = service.extract_health_claims(tweets)

    assert len(results) == 1
    assert "Exercise reduces heart disease risk" in results


def test_extract_health_claims_empty_tweets(app, service):
    """Test extraction with empty tweet list"""
    with app.app_context():
        results = service.extract_health_claims([])
    assert len(results) == 0


def test_extract_health_claims_filters_low_confidence(app, service):
    """Test that claims with low confidence are filtered out"""
    low_confidence_response = {
        "message": {
            "content": """
            {
                "claims": [
                    {
                        "text": "Maybe exercise is good",
                        "confidence": 0.5
                    }
                ]
            }
            """
        }
    }

    tweets = ["Maybe exercise is good for you"]

    with app.app_context():
        with patch("ollama.chat", return_value=low_confidence_response):
            results = service.extract_health_claims(tweets)

    assert len(results) == 0


def test_extract_health_claims_handles_error(app, service, mock_app_context):
    """Test error handling during extraction"""
    tweets = ["Some tweet"]

    with app.app_context():
        with patch("ollama.chat", side_effect=Exception("API Error")):
            results = service.extract_health_claims(tweets)

    assert len(results) == 0
    mock_app_context.error.assert_called()


def test_extract_health_claims_multiple_tweets(app, service, mock_ollama_response):
    """Test extraction from multiple tweets"""
    tweets = [
        "Exercise reduces heart disease risk",
        "Just a normal tweet",
        "Another health claim",
    ]

    with app.app_context():
        with patch("ollama.chat", return_value=mock_ollama_response):
            results = service.extract_health_claims(tweets)

    assert len(results) > 0
