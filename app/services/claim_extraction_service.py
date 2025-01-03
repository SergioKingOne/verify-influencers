from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class ClaimExtractionService:
    def __init__(self):
        # Load the pre-trained BioBERT model and tokenizer
        model_name = "dmis-lab/biobert-v1.1"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Set the device (CPU or GPU if available)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def extract_claims(self, tweets, threshold=0.5):
        """
        Extracts health claims from a list of tweets.

        Args:
            tweets: A list of strings (tweets).
            threshold: The probability threshold above which a tweet is considered a claim.

        Returns:
            A list of strings (the extracted claims).
        """
        claims = []
        for tweet in tweets:
            inputs = self.tokenizer(
                tweet,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512,  # Ensure input length is within model's limit
            )
            inputs = {
                key: val.to(self.device) for key, val in inputs.items()
            }  # Move inputs to device

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)[0]  # Get probabilities

            # Assuming the model's output is [not_claim, claim]
            if probs[1] > threshold:
                claims.append(tweet)

        return claims


# Example usage (for testing)
if __name__ == "__main__":
    service = ClaimExtractionService()
    example_tweets = [
        "New study shows that eating broccoli prevents cancer. #health #broccoli",
        "I'm feeling great today! The weather is beautiful.",
        "Taking vitamin C daily boosts your immune system.",
        "This is just a random tweet about nothing in particular.",
        "Clinical trials indicate that this new drug is highly effective in treating diabetes",
    ]
    extracted_claims = service.extract_claims(example_tweets)
    for claim in extracted_claims:
        print(f"- {claim}")
