from flask import Blueprint, render_template, current_app
from app.services.twitter_service import TwitterService
from app.services.claim_extraction_service import ClaimExtractionService

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

    if tweets is None:
        tweets = []
    if health_claims is None:
        health_claims = []

    return render_template("detail.html", tweets=tweets, health_claims=health_claims)
