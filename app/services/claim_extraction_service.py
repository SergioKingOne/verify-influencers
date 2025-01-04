import ollama
from flask import current_app


class ClaimExtractionService:
    def __init__(self):
        self.model_name = "llama3.2:3b"
        current_app.logger.info(
            f"Initialized ClaimExtractionService with model: {self.model_name}"
        )

    def extract_health_claims(self, tweets):
        """
        Extracts potential health claims from a list of tweets.
        """
        health_claims = []
        current_app.logger.info(
            f"Starting health claim extraction for {len(tweets)} tweets"
        )

        for tweet in tweets:
            prompt = f"""
            Identify the health claim in the following tweet, if any. 
            Answer with the health claim extracted word by word. 
            If there is no health claim, answer with 'No health claim found.'.

            Tweet: {tweet}

            Health Claim:
            """
            try:
                response = ollama.chat(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                )

                claim = response["message"]["content"].strip()

                if claim.lower() != "no health claim found.":
                    current_app.logger.info(f"Found health claim: {claim}")
                    health_claims.append(claim)

            except Exception as e:
                current_app.logger.error(f"Error during claim extraction: {str(e)}")
                current_app.logger.error(f"Failed tweet: {tweet}")

        current_app.logger.info(f"Extracted {len(health_claims)} health claims")
        return health_claims


# Example usage (you can test this outside the class for now)
if __name__ == "__main__":
    service = ClaimExtractionService()
    example_tweets = [
        "Eating more fruits and vegetables can improve your immune system.",
        "Just saw a beautiful sunset today!",
        "New study shows that exercise reduces the risk of heart disease.",
    ]
    extracted_claims = service.extract_health_claims(
        example_tweets
    )  # Corrected method name
    for claim in extracted_claims:
        print(claim)
