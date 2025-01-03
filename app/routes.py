from flask import Blueprint, render_template, current_app  # Import current_app
from app.services.twitter_service import TwitterService

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/influencer")
def influencer_detail():
    # Create TwitterService instance within the app context
    with current_app.app_context():
        twitter_service = TwitterService()
        tweets = twitter_service.get_tweets(
            "hubermanlab", 50
        )  # Fetch tweets (replace with your influencer)

    # Handle the case where tweets are None (due to an error)
    if tweets is None:
        tweets = []  # Or you could display an error message on the page

    return render_template("detail.html", tweets=tweets)
