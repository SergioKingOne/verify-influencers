from flask import Blueprint, render_template, current_app, flash
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
    tweets = []
    health_claims = []
    verification_results = {}
    username = "hubermanlab"  # This could be made dynamic via query parameter

    try:
        with current_app.app_context():
            # Get tweets and user info
            twitter_service = TwitterService()
            user_info = twitter_service.get_user_info(username)
            tweets = twitter_service.get_tweets(username, 10)

            if tweets is None:
                flash(
                    "Unable to fetch tweets. Twitter API rate limit may have been exceeded.",
                    "error",
                )
                return render_template(
                    "detail.html",
                    tweets=[],
                    health_claims=[],
                    verification_results={},
                    error=True,
                )

            # Extract and process claims
            claim_extraction_service = ClaimExtractionService()
            health_claims = claim_extraction_service.extract_health_claims(tweets)

            if health_claims:
                data_processing_service = DataProcessingService()
                unique_claims = data_processing_service.remove_duplicate_claims(
                    health_claims
                )

                claim_verification_service = ClaimVerificationService()
                for claim in unique_claims:
                    verification_results[claim] = (
                        claim_verification_service.verify_claim(claim)
                    )

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        current_app.logger.error(f"Error in influencer_detail: {str(e)}")

    return render_template(
        "detail.html",
        username=username,
        profile_image=user_info.get("profile_image") if user_info else None,
        follower_count=user_info.get("follower_count") if user_info else None,
        tweets=tweets or [],
        health_claims=health_claims or [],
        verification_results=verification_results,
        error=False,
    )
