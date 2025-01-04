from typing import List, Dict, Any
from pymed import PubMed
from sentence_transformers import SentenceTransformer, util
from flask import current_app


class ClaimVerificationService:
    def __init__(self):
        self.pubmed = PubMed(
            tool="HealthClaimVerifier", email="sergiorobayoro@example.com"
        )  # Replace with your email
        self.similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
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
            articles = [
                {
                    "title": article.title,
                    "abstract": article.abstract,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{article.pmid}/",
                }
                for article in results
            ]
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

    def verify_claim(self, claim, max_results=5, similarity_threshold=0.3):
        """
        Verifies a health claim against PubMed articles.

        Args:
            claim: The health claim string.
            max_results: The maximum number of PubMed articles to retrieve.
            similarity_threshold: The minimum similarity score to consider an abstract as supporting evidence.

        Returns:
            A dictionary with:
                - verification_status: (str) "Verified", "Questionable", or "Debunked"
                - supporting_evidence: (list) List of abstracts that support the claim.
                - contradicting_evidence: (list) List of abstracts that contradict the claim.
                - pubmed_results: (list) The raw PubMed search results.
        """
        pubmed_results = self.search_pubmed(claim, max_results)

        supporting_evidence = []
        contradicting_evidence = []

        for article in pubmed_results:
            similarity = self.calculate_similarity(claim, article["abstract"])

            if similarity >= similarity_threshold:
                supporting_evidence.append(article["abstract"])
            else:
                contradicting_evidence.append(article["abstract"])

        if len(supporting_evidence) >= 2:
            verification_status = "Verified"
        elif len(supporting_evidence) > 0:
            verification_status = "Questionable"
        else:
            verification_status = "Debunked"

        return {
            "verification_status": verification_status,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": contradicting_evidence,
            "pubmed_results": pubmed_results,
        }
