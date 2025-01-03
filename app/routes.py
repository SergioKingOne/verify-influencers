# app/routes.py
from flask import Blueprint, render_template, current_app
from app.services.twitter_service import TwitterService
from app.services.claim_extraction_service import ClaimExtractionService
from app.services.claim_verification_service import ClaimVerificationService
from app.services.data_processing_service import DataProcessingService

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/influencer")
def influencer_detail():
    with current_app.app_context():
        twitter_service = TwitterService()
        tweets = twitter_service.get_tweets("hubermanlab", 50)

        claim_extraction_service = ClaimExtractionService()
        health_claims = claim_extraction_service.extract_health_claims(tweets)

        data_processing_service = DataProcessingService()
        unique_claims = data_processing_service.remove_duplicate_claims(health_claims)

        claim_verification_service = ClaimVerificationService()

        verification_results = {}
        for claim in unique_claims:
            verification_results[claim] = claim_verification_service.verify_claim(claim)

    if tweets is None:
        tweets = []
    if health_claims is None:
        health_claims = []

    return render_template(
        "detail.html",
        tweets=tweets,
        health_claims=health_claims,
        verification_results=verification_results,
    )
