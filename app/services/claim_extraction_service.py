# app/services/claim_extraction_service.py
import ollama


class ClaimExtractionService:
    def __init__(self):
        self.model_name = "llama3.2:3b"

    def extract_health_claims(self, tweets):
        """
        Extracts potential health claims from a list of tweets.

        Args:
            tweets: A list of strings (tweets).

        Returns:
            A list of strings (potential health claims).
        """
        health_claims = []
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
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                )

                claim = response["message"]["content"].strip()

                if claim.lower() != "no health claim found.":
                    health_claims.append(claim)
            except Exception as e:
                print(f"Error during claim extraction: {e}")
                # Handle the error appropriately (e.g., log it, return an empty list, etc.)

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
