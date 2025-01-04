import pytest
from flask import Flask
from app.services.claim_extraction_service import ClaimExtractionService
from app.utils.logger import setup_logger


@pytest.fixture
def app():
    """Create a Flask app for testing"""
    app = Flask(__name__)
    # Setup logger for testing
    setup_logger(app)
    return app


@pytest.fixture
def service(app):
    """Create actual ClaimExtractionService instance"""
    with app.app_context():
        return ClaimExtractionService()


@pytest.mark.integration
def test_real_health_claim_extraction(app, service):
    """Test extraction of health claims using actual ollama model"""
    app.logger.info("Starting test_real_health_claim_extraction")
    tweets = [
        "A new study shows that getting 8 hours of sleep improves memory and cognitive function.",
        "Just had a great cup of coffee!",  # Non-health tweet
        "Regular exercise has been proven to reduce anxiety and depression by 30%.",
    ]

    with app.app_context():
        app.logger.info(f"Processing {len(tweets)} tweets")
        results = service.extract_health_claims(tweets)
        app.logger.info(f"Extracted claims: {results}")

    assert len(results) > 0
    app.logger.info("Verifying extracted claims")
    # Verify we got health claims but not the coffee tweet
    assert any("sleep" in claim.lower() for claim in results)
    assert any("exercise" in claim.lower() for claim in results)
    assert not any("coffee" in claim.lower() for claim in results)
    app.logger.info("Test completed successfully")


@pytest.mark.integration
def test_complex_health_claims(app, service):
    """Test extraction of more complex health claims"""
    app.logger.info("Starting test_complex_health_claims")
    tweets = [
        "Research indicates that intermittent fasting combined with regular exercise can improve metabolic health and longevity.",
        "A meta-analysis of 50 studies shows that meditation practice for 10 minutes daily reduces stress levels by 25%.",
    ]

    with app.app_context():
        app.logger.info(f"Processing {len(tweets)} complex tweets")
        results = service.extract_health_claims(tweets)
        app.logger.info(f"Extracted complex claims: {results}")

    assert len(results) >= 2
    app.logger.info("Checking for health-related keywords")
    health_keywords = ["fasting", "exercise", "meditation", "stress"]
    found_keywords = [
        any(keyword in claim.lower() for claim in results)
        for keyword in health_keywords
    ]
    app.logger.info(
        f"Keywords found: {[k for i, k in enumerate(health_keywords) if found_keywords[i]]}"
    )
    assert any(found_keywords), "Should find at least some health-related keywords"
    app.logger.info("Complex claims test completed successfully")


@pytest.mark.integration
def test_non_health_claims(app, service):
    """Test that non-health tweets are properly filtered"""
    tweets = [
        "Beautiful sunset today!",
        "Just finished reading a great book.",
        "Traffic was terrible this morning.",
    ]

    with app.app_context():
        results = service.extract_health_claims(tweets)

    assert len(results) == 0, "Non-health tweets should not generate health claims"


@pytest.mark.integration
def test_mixed_claims_batch(app, service):
    """Test processing a mixed batch of health and non-health tweets"""
    tweets = [
        "New research suggests vitamin D supplementation may boost immune function.",
        "Excited for the weekend!",
        "Studies show that high-intensity interval training burns more calories than steady-state cardio.",
        "Just watched an amazing movie.",
    ]

    with app.app_context():
        results = service.extract_health_claims(tweets)

    assert len(results) >= 2
    assert any("vitamin" in claim.lower() for claim in results)
    assert any(
        "training" in claim.lower() or "cardio" in claim.lower() for claim in results
    )


@pytest.mark.integration
def test_confidence_threshold(app, service):
    """Test that the confidence threshold is working with real model outputs"""
    tweets = [
        "Maybe drinking green tea might help with weight loss?",  # Uncertain claim
        "Studies definitively prove that regular exercise improves cardiovascular health.",  # Certain claim
    ]

    with app.app_context():
        results = service.extract_health_claims(tweets)

    # The uncertain claim should be filtered out due to low confidence
    assert any("exercise" in claim.lower() for claim in results)
    assert not any("tea" in claim.lower() for claim in results)
