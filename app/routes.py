from flask import Blueprint, render_template, current_app
from app.services.twitter_service import TwitterService
from app.services.claim_extraction_service import ClaimExtractionService

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/influencer")
def influencer_detail():
    # Create service instances within the app context
    with current_app.app_context():
        twitter_service = TwitterService()
        tweets = twitter_service.get_tweets("hubermanlab", 50)
        claim_extraction_service = ClaimExtractionService()
        claims = claim_extraction_service.extract_claims(tweets)

    if tweets is None:
        tweets = []

    # Pass both tweets and claims to the template
    return render_template("detail.html", tweets=tweets, claims=claims)
