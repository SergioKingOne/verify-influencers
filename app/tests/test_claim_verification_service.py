import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from app.services.claim_verification_service import ClaimVerificationService


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
def mock_pubmed_article():
    """Create a mock PubMed article"""
    article = MagicMock()
    article.pubmed_id = "12345"
    article.title = "Test Article"
    article.abstract = "This is a test abstract about exercise and health."
    return article


@pytest.fixture
def service(mock_app_context):
    """Create ClaimVerificationService instance with mocked dependencies"""
    with patch("pymed.PubMed"), patch("sentence_transformers.SentenceTransformer"):
        service = ClaimVerificationService()
        return service


def test_search_pubmed_successful(app, service, mock_pubmed_article):
    """Test successful PubMed search"""
    with app.app_context():
        with patch.object(service.pubmed, "query", return_value=[mock_pubmed_article]):
            results = service.search_pubmed("exercise health")

    assert len(results) == 1
    assert results[0]["title"] == "Test Article"
    assert "pubmed.ncbi.nlm.nih.gov/12345" in results[0]["url"]


def test_search_pubmed_handles_error(app, service, mock_app_context):
    """Test error handling in PubMed search"""
    with app.app_context():
        with patch.object(
            service.pubmed, "query", side_effect=Exception("PubMed Error")
        ):
            results = service.search_pubmed("test query")

    assert len(results) == 0
    mock_app_context.error.assert_called()


def test_calculate_similarity(app, service):
    """Test similarity calculation"""
    with app.app_context():
        with patch.object(service.similarity_model, "encode") as mock_encode:
            mock_encode.return_value = Mock()
            with patch(
                "sentence_transformers.util.pytorch_cos_sim",
                return_value=Mock(item=lambda: 0.8),
            ):
                similarity = service.calculate_similarity(
                    "Exercise reduces heart disease",
                    "Studies show exercise benefits heart health",
                )

    assert 0 <= similarity <= 1


def test_verify_claim_verified(app, service, mock_pubmed_article):
    """Test claim verification with supporting evidence"""
    with app.app_context():
        with patch.object(
            service.pubmed,
            "query",
            return_value=[mock_pubmed_article, mock_pubmed_article],
        ):
            with patch.object(service, "calculate_similarity", return_value=0.8):
                result = service.verify_claim("Exercise is good for health")

    assert result["verification_status"] == "Verified"
    assert len(result["supporting_evidence"]) >= 2


def test_verify_claim_debunked(app, service, mock_pubmed_article):
    """Test claim verification with no supporting evidence"""
    with app.app_context():
        with patch.object(service.pubmed, "query", return_value=[mock_pubmed_article]):
            with patch.object(service, "calculate_similarity", return_value=0.1):
                result = service.verify_claim("Invalid health claim")

    assert result["verification_status"] == "Debunked"
    assert len(result["supporting_evidence"]) == 0


def test_calculate_trust_score(app, service):
    """Test trust score calculation"""
    verification_results = {
        "claim1": {"verification_status": "Verified"},
        "claim2": {"verification_status": "Debunked"},
        "claim3": {"verification_status": "Verified"},
    }

    with app.app_context():
        score, total_claims = service.calculate_trust_score(verification_results)

    assert 0 <= score <= 100
    assert total_claims == 3
