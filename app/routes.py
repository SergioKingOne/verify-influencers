from flask import Blueprint, jsonify, current_app
from app.services.twitter_service import TwitterService
from app.services.claim_extraction_service import ClaimExtractionService
from app.services.claim_verification_service import ClaimVerificationService
from app.services.data_processing_service import DataProcessingService

main = Blueprint("main", __name__)


@main.route("/api/influencer/<username>")
def influencer_detail(username):
    try:
        with current_app.app_context():
            # Get tweets and user info
            twitter_service = TwitterService()
            user_info = twitter_service.get_user_info(username)
            tweets = twitter_service.get_tweets(username, 20)

            if tweets is None:
                return (
                    jsonify(
                        {
                            "error": "Unable to fetch tweets. Twitter API rate limit may have been exceeded."
                        }
                    ),
                    429,
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
                verification_results = {}
                for claim in unique_claims:
                    verification_results[claim] = (
                        claim_verification_service.verify_claim(claim)
                    )

            # Calculate trust score
            trust_score, total_claims = (
                claim_verification_service.calculate_trust_score(verification_results)
            )

            return jsonify(
                {
                    "username": username,
                    "profile_image": (
                        user_info.get("profile_image") if user_info else None
                    ),
                    "follower_count": (
                        user_info.get("follower_count") if user_info else None
                    ),
                    "tweets": tweets,
                    "health_claims": health_claims,
                    "verification_results": verification_results,
                    "trust_score": trust_score,
                    "total_claims": total_claims,
                }
            )

    except Exception as e:
        current_app.logger.error(f"Error in influencer_detail: {str(e)}")
        return jsonify({"error": str(e)}), 500
