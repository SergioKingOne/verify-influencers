import ollama
from flask import current_app
from pydantic import BaseModel
from typing import List, Optional


class HealthClaim(BaseModel):
    claim: str
    confidence: float = 1.0  # Default confidence score


class HealthClaimsResponse(BaseModel):
    claims: List[HealthClaim]


class ClaimExtractionService:
    def __init__(self):
        self.model_name = "llama3.2:3b"
        current_app.logger.info(
            f"Initialized ClaimExtractionService with model: {self.model_name}"
        )

    def extract_health_claims(self, tweets: List[str]) -> List[str]:
        """
        Extracts potential health claims from a list of tweets using structured output.
        """
        health_claims = []
        current_app.logger.info(
            f"Starting health claim extraction for {len(tweets)} tweets"
        )

        for tweet in tweets:
            prompt = f"""
            Identify any health claims made by the author in the following tweet. For each claim, rate your confidence (0.0-1.0) in the scientific validity of the claim based on current medical consensus.
            
            A confidence of:
            - 1.0: Strongly supported by multiple peer-reviewed studies
            - 0.7-0.9: Supported by some scientific evidence
            - 0.4-0.6: Limited or mixed scientific evidence
            - 0.0-0.3: Little to no scientific support or contradicts current evidence
            
            Tweet: {tweet}
            
            Respond using JSON format.
            """
            try:
                response = ollama.chat(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    format=HealthClaimsResponse.model_json_schema(),
                    options={
                        "temperature": 0.1
                    },  # Lower temperature for more consistent outputs
                )

                # Parse and validate response using Pydantic
                claims_response = HealthClaimsResponse.model_validate_json(
                    response["message"]["content"]
                )

                # Add claims with sufficient confidence
                for claim in claims_response.claims:
                    if claim.confidence >= 0.7:  # Only include high confidence claims
                        current_app.logger.info(
                            f"Found health claim: {claim.claim} (confidence: {claim.confidence})"
                        )
                        health_claims.append(claim.claim)

            except Exception as e:
                current_app.logger.error(f"Error during claim extraction: {str(e)}")
                current_app.logger.error(f"Failed tweet: {tweet}")

        current_app.logger.info(f"Extracted {len(health_claims)} health claims")
        return health_claims


# Example usage
if __name__ == "__main__":
    service = ClaimExtractionService()
    example_tweets = [
        "Eating more fruits and vegetables can improve your immune system.",
        "Just saw a beautiful sunset today!",
        "New study shows that exercise reduces the risk of heart disease.",
    ]
    extracted_claims = service.extract_health_claims(example_tweets)
    for claim in extracted_claims:
        print(claim)
