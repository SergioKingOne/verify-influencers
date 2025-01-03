import tweepy
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

    def get_tweets(self, username, num_tweets=50):
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
                print(f"Error: No user found with username '{username}'.")
                return None
            user_id = user.data.id

            response = self.client.get_users_tweets(
                id=user_id,
                max_results=num_tweets,
                exclude=["retweets", "replies"],  # Exclude retweets and replies for now
            )

            tweets = [tweet.text for tweet in response.data]
            return tweets

        except tweepy.TweepyException as e:
            print(f"Error fetching tweets: {e}")
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
