from typing import List, Dict, Any
from pymed import PubMed
from sentence_transformers import SentenceTransformer, util
from flask import current_app
import json
import ollama
from pydantic import BaseModel
from enum import Enum


class VerificationStatus(str, Enum):
    VERIFIED = "Verified"
    QUESTIONABLE = "Questionable"
    DEBUNKED = "Debunked"


class VerificationResponse(BaseModel):
    verification_status: VerificationStatus
    explanation: str
    supporting_points: List[str]
    contradicting_points: List[str]
    pubmed_results: List[Dict[str, str]]


class ClaimVerificationService:
    def __init__(self):
        self.pubmed = PubMed(
            tool="HealthClaimVerifier", email="sergiorobayoro@example.com"
        )  # Replace with your email
        self.similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.model_name = "llama3.2:3b"
        current_app.logger.info("Initialized ClaimVerificationService")

    def search_pubmed(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Searches PubMed for articles related to a query.

        Args:
            query: The search query string.
            max_results: The maximum number of results to return.

        Returns:
            A list of PubMed articles with title, abstract, and URL.

        Raises:
            PubMedSearchError: If there's an error accessing PubMed.
        """
        try:
            current_app.logger.info(f"Searching PubMed for: {query}")
            results = self.pubmed.query(query, max_results=max_results)
            articles = []

            for article in results:
                try:
                    # Safely extract PMID
                    pmid = getattr(article, "pubmed_id", None)
                    if not pmid:
                        continue

                    articles.append(
                        {
                            "title": article.title if hasattr(article, "title") else "",
                            "abstract": (
                                article.abstract if hasattr(article, "abstract") else ""
                            ),
                            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        }
                    )
                except AttributeError as e:
                    current_app.logger.warning(
                        f"Skipping article due to missing attribute: {e}"
                    )
                    continue

            current_app.logger.info(f"Found {len(articles)} PubMed articles")
            return articles

        except Exception as e:
            current_app.logger.error(f"Error searching PubMed: {e}")
            return []

    def calculate_similarity(self, claim, abstract):
        """
        Calculates the cosine similarity between a claim and an abstract using a Sentence Transformer model.

        Args:
            claim: The health claim string.
            abstract: The abstract string.

        Returns:
            A similarity score (float) between 0 and 1.
        """
        if not abstract:  # Handle cases where the abstract might be empty or None
            return 0.0

        claim_embedding = self.similarity_model.encode(claim, convert_to_tensor=True)
        abstract_embedding = self.similarity_model.encode(
            abstract, convert_to_tensor=True
        )
        similarity = util.pytorch_cos_sim(claim_embedding, abstract_embedding).item()
        return similarity

    def verify_claim(self, claim, max_results=5):
        """
        Verifies a health claim by searching PubMed articles and using LLM to analyze them.

        Args:
            claim: The health claim string.
            max_results: The maximum number of PubMed articles to retrieve.

        Returns:
            A dictionary with verification results and evidence.
        """
        pubmed_results = self.search_pubmed(claim, max_results)

        if not pubmed_results:
            return VerificationResponse(
                verification_status=VerificationStatus.QUESTIONABLE,
                explanation="No relevant research articles found",
                supporting_points=[],
                contradicting_points=[],
                pubmed_results=[],
            ).model_dump()

        prompt = f"""
        Analyze this health claim against the following research articles:

        CLAIM: {claim}

        RESEARCH ARTICLES:
        """

        for i, article in enumerate(pubmed_results, 1):
            prompt += f"""
            Article {i}:
            Title: {article['title']}
            Abstract: {article['abstract']}
            Source: {article['url']}
            """

        prompt += """
        Based on these research articles, determine if the claim is:
        - "Verified" (strong scientific support)
        - "Questionable" (limited or mixed evidence)
        - "Debunked" (contradicts evidence)
        """

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                format=VerificationResponse.model_json_schema(),
                options={"temperature": 0.1},
            )

            # Parse and validate response using Pydantic
            verification_response = VerificationResponse.model_validate_json(
                response["message"]["content"]
            )

            # Add PubMed results
            verification_response.pubmed_results = pubmed_results

            return verification_response.model_dump()

        except Exception as e:
            current_app.logger.error(f"Error during claim verification: {str(e)}")
            return VerificationResponse(
                verification_status=VerificationStatus.QUESTIONABLE,
                explanation=f"Error during verification: {str(e)}",
                supporting_points=[],
                contradicting_points=[],
                pubmed_results=pubmed_results,
            ).model_dump()

    def calculate_trust_score(self, verification_results):
        """
        Calculates a trust score based on verification results.

        Scoring system:
        - Verified: +2 points
        - Questionable: +0 points
        - Debunked: -1 point

        Returns:
        - score: 0-100 scale
        - total_claims: number of claims analyzed
        """
        if not verification_results:
            return 0, 0

        points = 0
        total_claims = len(verification_results)

        for result in verification_results.values():
            status = result.get("verification_status", "")
            if status == "Verified":
                points += 2
            elif status == "Debunked":
                points -= 1

        # Convert to 0-100 scale
        max_possible = total_claims * 2  # If all claims were verified
        if max_possible == 0:
            return 0, 0

        normalized_score = min(100, max(0, (points / max_possible) * 100))
        return round(normalized_score), total_claims
