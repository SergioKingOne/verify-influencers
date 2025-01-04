import pytest
from flask import Flask
from app.services.claim_verification_service import ClaimVerificationService


@pytest.fixture
def app():
    """Create a Flask app for testing"""
    app = Flask(__name__)
    return app


@pytest.fixture
def service(app):
    """Create actual ClaimVerificationService instance"""
    with app.app_context():
        return ClaimVerificationService()


@pytest.mark.integration
def test_real_pubmed_search(app, service):
    """Test actual PubMed search functionality"""
    with app.app_context():
        results = service.search_pubmed("exercise cardiovascular health", max_results=3)

    assert len(results) > 0
    assert all(isinstance(article["title"], str) for article in results)
    assert all(isinstance(article["abstract"], str) for article in results)
    assert all(isinstance(article["url"], str) for article in results)


@pytest.mark.integration
def test_real_claim_verification(app, service):
    """Test verification of a real health claim"""
    claim = "Regular exercise reduces the risk of cardiovascular disease"

    with app.app_context():
        result = service.verify_claim(claim, max_results=3)

    assert "verification_status" in result
    assert "supporting_evidence" in result
    assert "pubmed_results" in result
    assert len(result["pubmed_results"]) > 0


@pytest.mark.integration
def test_verification_with_questionable_claim(app, service):
    """Test verification of a questionable health claim"""
    claim = "Drinking water cures all diseases"

    with app.app_context():
        result = service.verify_claim(claim, max_results=3)

    assert result["verification_status"] in ["Questionable", "Debunked"]
