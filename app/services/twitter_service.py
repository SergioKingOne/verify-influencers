import tweepy
from flask import current_app
from app import create_app


class TwitterService:
    def __init__(self):
        # Use the app's configuration to get the API keys
        app = create_app()  # Create app context to access config
        self.api_key = app.config["TWITTER_API_KEY"]
        self.api_secret = app.config["TWITTER_API_SECRET"]
        self.bearer_token = app.config["TWITTER_BEARER_TOKEN"]

        # Initialize the Tweepy client
        self.client = tweepy.Client(bearer_token=self.bearer_token)

    def get_tweets(self, username: str, num_tweets: int = 50) -> list[str] | None:
        """
        Fetches the most recent tweets from a given user.

        Args:
            username: The Twitter handle of the user (without the @).
            num_tweets: The number of tweets to fetch (default is 50).

        Returns:
            A list of strings, where each string is a tweet.
            Returns None if there's an error.
        """
        try:
            # The new Twitter v2 API uses user ID instead of screen name
            user = self.client.get_user(username=username)
            if user.data is None:
                current_app.logger.error(f"No user found with username '{username}'")
                return None
            user_id = user.data.id

            current_app.logger.info(f"Fetching {num_tweets} tweets for user {username}")

            response = self.client.get_users_tweets(
                id=user_id,
                max_results=num_tweets,
                exclude=["retweets", "replies"],  # Exclude retweets and replies for now
            )

            tweets = [tweet.text for tweet in response.data]
            current_app.logger.info(f"Successfully fetched {len(tweets)} tweets")
            return tweets

        except tweepy.TooManyRequests as e:
            current_app.logger.error(f"Rate limit exceeded: {e}")
            return None
        except tweepy.NotFound as e:
            current_app.logger.error(f"User '{username}' not found: {e}")
            return None
        except tweepy.TweepyException as e:
            current_app.logger.error(f"Twitter API error: {e}")
            return None

    def get_user_info(self, username: str) -> dict:
        """
        Fetches user profile information.

        Args:
            username: The Twitter handle of the user (without the @)

        Returns:
            Dictionary containing user information including profile image and follower count
        """
        try:
            user = self.client.get_user(
                username=username, user_fields=["profile_image_url", "public_metrics"]
            )

            current_app.logger.info(f"User info: {user.data}")

            if user.data is None:
                current_app.logger.error(f"No user found with username '{username}'")
                return None

            return {
                "profile_image": user.data.profile_image_url,
                "follower_count": user.data.public_metrics["followers_count"],
            }

        except Exception as e:
            current_app.logger.error(f"Error fetching user info: {e}")
            return None


# Example usage (you can test this outside the class for now)
if __name__ == "__main__":
    twitter_service = TwitterService()
    tweets = twitter_service.get_tweets(
        "hubermanlab", 10
    )  # Replace with your influencer

    if tweets:
        for i, tweet in enumerate(tweets):
            print(f"{i+1}: {tweet}\n")
