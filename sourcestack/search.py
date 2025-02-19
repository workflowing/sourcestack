import os
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
from collections import Counter
from sourcestack.client import Client
from sourcestack.exceptions import SearchError


class SourceStackSearchService:
    """Service for searching SourceStack Jobs"""

    SEARCH_PARAMS = {
        "name",
        "url",
        "parent",
        "uses_product",
        "uses_category",
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the search service

        Args:
            api_key: Optional API key (defaults to SOURCESTACK_API_KEY env var)
            base_url: Optional base URL (defaults to SOURCESTACK_BASE_URL env var)
        """
        self.api_key = api_key or os.getenv("SOURCESTACK_API_KEY")
        self.base_url = base_url or os.getenv("SOURCESTACK_BASE_URL")

        if not self.api_key:
            raise SearchError(
                "No API key provided and SOURCESTACK_API_KEY environment variable not set"
            )

        self.client = Client(api_key=self.api_key, base_url=self.base_url)

    def _validate_search_params(self, params: Dict[str, Any]) -> None:
        """Validate search parameters"""
        search_params_used = [param for param in self.SEARCH_PARAMS if param in params]
        if len(search_params_used) != 1:
            raise SearchError(
                f"Exactly one search parameter required from: {self.SEARCH_PARAMS}"
            )

    def _process_url(self, url: str) -> str:
        """Process URL by removing common prefixes"""
        url = url.replace("https://", "").replace("http://", "")
        return url.replace("www.", "")

    def _format_results(
        self,
        results: List[Dict[str, Any]],
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Format the search results with statistics"""
        if not results:
            return {
                "status": "error",
                "message": "No results found",
                "timestamp": datetime.now().isoformat(),
                "count": 0,
            }

        # Collect statistics
        companies = Counter(
            str(result.get("company_name", "Unknown")) for result in results
        )
        technologies = Counter(
            tech for result in results for tech in result.get("tags_matched", [])
        )
        categories = Counter(
            category
            for result in results
            for category in result.get("tag_categories", [])
        )

        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "count": len(results),
            "statistics": {
                "companies": [
                    {"name": k, "count": v} for k, v in companies.most_common(5)
                ],
                "technologies": [
                    {"name": k, "count": v} for k, v in technologies.most_common(5)
                ],
                "categories": [
                    {"name": k, "count": v} for k, v in categories.most_common(5)
                ],
            },
            "entries": results,
        }

        return response

    def search_jobs(self, **kwargs) -> Dict[str, Any]:
        """Search for jobs using the SourceStack API

        Args:
            name (str, optional): Search by job name
            url (str, optional): Search by company URL
            parent (str, optional): Search by parent company
            uses_product (str, optional): Search by product usage
            uses_category (str, optional): Search by product category
            exact (bool, optional): Whether to do exact matching (default varies by endpoint)
            limit (int, optional): Maximum number of results to return

        Returns:
            Dict containing search results and metadata
        """
        try:
            self._validate_search_params(kwargs)

            # Process URL if provided
            if url := kwargs.get("url"):
                kwargs["url"] = self._process_url(url)

            # Determine which search method to use and execute
            if "name" in kwargs:
                exact = kwargs.pop("exact", False)
                results = self.client.jobs.by_name(
                    kwargs.pop("name"), exact=exact, **kwargs
                )
            elif "url" in kwargs:
                results = self.client.jobs.by_url(kwargs.pop("url"), **kwargs)
            elif "parent" in kwargs:
                results = self.client.jobs.by_parent(kwargs.pop("parent"), **kwargs)
            elif "uses_product" in kwargs:
                exact = kwargs.pop("exact", True)
                results = self.client.jobs.by_uses_product(
                    kwargs.pop("uses_product"), exact=exact, **kwargs
                )
            elif "uses_category" in kwargs:
                exact = kwargs.pop("exact", True)
                results = self.client.jobs.by_uses_category(
                    kwargs.pop("uses_category"), exact=exact, **kwargs
                )

            # Format results with statistics
            response = self._format_results(results["data"], limit=kwargs.get("limit"))

            # Add pagination if limit was specified
            if limit := kwargs.get("limit"):
                response["pagination"] = {
                    "limit": limit,
                    "total": len(results["data"]),
                }

            return response

        except Exception as e:
            raise SearchError(f"Search failed: {str(e)}") from e
