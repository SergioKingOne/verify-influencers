from sentence_transformers import SentenceTransformer, util
from flask import current_app


class DataProcessingService:
    def __init__(self):
        self.similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
        current_app.logger.info(
            "Initialized DataProcessingService with SentenceTransformer"
        )

    def remove_duplicate_claims(self, claims, similarity_threshold=0.8):
        """
        Removes duplicate health claims based on semantic similarity.

        Args:
            claims: A list of health claim strings.
            similarity_threshold: The minimum similarity score to consider two claims as duplicates.

        Returns:
            A list of unique health claims.
        """
        current_app.logger.info(f"Processing {len(claims)} claims for duplicates")
        unique_claims = []

        for claim in claims:
            is_duplicate = False
            for existing_claim in unique_claims:
                similarity = self.calculate_similarity(claim, existing_claim)
                if similarity >= similarity_threshold:
                    current_app.logger.info(
                        f"Found duplicate claim: '{claim}' similar to '{existing_claim}' (score: {similarity:.2f})"
                    )
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_claims.append(claim)

        current_app.logger.info(f"Reduced to {len(unique_claims)} unique claims")
        return unique_claims

    def calculate_similarity(self, claim1, claim2):
        """
        Calculates the cosine similarity between two claims using a Sentence Transformer model.

        Args:
            claim1: The first health claim string.
            claim2: The second health claim string.

        Returns:
            A similarity score (float) between 0 and 1.
        """
        try:
            claim1_embedding = self.similarity_model.encode(
                claim1, convert_to_tensor=True
            )
            claim2_embedding = self.similarity_model.encode(
                claim2, convert_to_tensor=True
            )
            similarity = util.pytorch_cos_sim(claim1_embedding, claim2_embedding).item()
            return similarity
        except Exception as e:
            current_app.logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
