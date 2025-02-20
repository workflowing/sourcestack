import os
from unittest.mock import Mock, patch

import pytest

from sourcestack.exceptions import SearchError
from sourcestack.search import SourceStackSearchService


@pytest.fixture
def search_service():
    api_key = os.getenv("SOURCESTACK_API_KEY")
    base_url = os.getenv("SOURCESTACK_BASE_URL")
    if not api_key:
        pytest.skip("SOURCESTACK_API_KEY environment variable not set")
    return SourceStackSearchService(api_key=api_key, base_url=base_url)


@pytest.fixture
def mock_search_service():
    with patch("sourcestack.search.Client") as mock_client:
        service = SourceStackSearchService(api_key="test_key", base_url="test_url")
        yield service, mock_client


@pytest.mark.integration
class TestJobSearchEndpoints:
    def test_jobs_search_by_name_contains(self, search_service):
        results = search_service.search_jobs(name="DevOps", exact=False, limit=2)
        assert results["status"] == "success"
        assert results["count"] > 0
        assert all("devops" in job["job_name"].lower() for job in results["entries"])

    def test_jobs_search_by_exact_name(self, search_service):
        results = search_service.search_jobs(name="Platform Engineer", exact=True)
        assert results["status"] == "success"
        assert all(
            job["job_name"].lower() == "platform engineer" for job in results["entries"]
        )

    def test_jobs_search_by_parent_company(self, search_service):
        results = search_service.search_jobs(parent="Spotify")
        assert results["status"] == "success"
        assert all(
            "spotify" in job["company_name"].lower() for job in results["entries"]
        )

    def test_jobs_search_by_url(self, search_service):
        results = search_service.search_jobs(url="canva.com")
        assert results["status"] == "success"
        assert all(
            "canva.com" in job["company_url"].lower() for job in results["entries"]
        )

    def test_jobs_search_by_product_use(self, search_service):
        results = search_service.search_jobs(uses_product="Docker", exact=True)
        assert results["status"] == "success"
        assert all(
            "docker" in [tag.lower() for tag in job["tags_matched"]]
            for job in results["entries"]
        )

    def test_jobs_search_by_category(self, search_service):
        results = search_service.search_jobs(uses_category="Container Orchestration")
        assert results["status"] == "success"
        assert all(
            "container orchestration" in [cat.lower() for cat in job["tag_categories"]]
            for job in results["entries"]
        )


class TestSearchValidation:
    def test_exact_parameter_validation(self, mock_search_service):
        service, _ = mock_search_service

        # Test valid exact parameter with name
        service._validate_search_params({"name": "DevOps", "exact": True})

        # Test valid exact parameter with uses_product
        service._validate_search_params({"uses_product": "Docker", "exact": True})

    def test_search_parameter_validation(self, mock_search_service):
        service, _ = mock_search_service

        # Test invalid - no search parameter
        with pytest.raises(SearchError):
            service._validate_search_params({})

        # Test invalid - multiple search parameters
        with pytest.raises(SearchError):
            service._validate_search_params({"name": "Engineer", "url": "company.com"})


class TestSearchResults:
    @pytest.mark.integration
    def test_search_results_limit(self, search_service):
        limit = 5
        results = search_service.search_jobs(name="developer", limit=limit)

        assert results["status"] == "success"
        assert len(results["entries"]) <= limit
        assert "pagination" in results
        assert results["pagination"]["limit"] == limit
