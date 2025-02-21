from typing import Any, Dict, List, Optional, TypedDict
from urllib.parse import urljoin

from sourcestack.resource import Resource

Job = Dict[str, Any]

Response = TypedDict(
    "Response",
    {
        "data": List[Job],
    },
)


class Jobs(Resource):
    def by_name(self, name: str, exact: bool = False, **kwargs) -> Response:
        """
        Fetches jobs by name from the SourceStack API.

        Args:
            name (str): The name of the job.
            exact (bool): Whether to match the name exactly.
            **kwargs: Additional query parameters (e.g., limit, fields)

        Returns:
            Response: A list of jobs.
        """
        params = {"name": name, "exact": "true" if exact else "false", **kwargs}
        return self._get(**params)

    def by_parent(self, parent: str, **kwargs) -> Response:
        """
        Fetches jobs by parent from the SourceStack API.

        Args:
            parent (str): The parent of the job.
            **kwargs: Additional query parameters (e.g., limit, fields)

        Returns:
            Response: A list of jobs.
        """
        params = {"parent": parent, **kwargs}
        return self._get(**params)

    def by_url(self, url: str, **kwargs) -> Response:
        """
        Fetches jobs by url from the SourceStack API.

        Args:
            url (str): The url of the job.
            **kwargs: Additional query parameters (e.g., limit, fields)

        Returns:
            Response: A list of jobs.
        """
        params = {"url": url, **kwargs}
        return self._get(**params)

    def by_uses_product(
        self, uses_product: str, exact: bool = True, **kwargs
    ) -> Response:
        """
        Fetches jobs by product from the SourceStack API.

        Args:
            product (str): The product of the job.
            exact (bool): Whether to match the product exactly.
            **kwargs: Additional query parameters (e.g., limit, fields)

        Returns:
            Response: A list of jobs.
        """
        params = {
            "uses_product": uses_product,
            "exact": "true" if exact else "false",
            **kwargs,
        }
        return self._get(**params)

    def by_uses_category(
        self, uses_category: str, exact: bool = True, **kwargs
    ) -> Response:
        """
        Fetches jobs by category from the SourceStack API.

        Args:
            category (str): The category of the job.
            exact (bool): Whether to match the category exactly.
            **kwargs: Additional query parameters (e.g., limit, fields)

        Returns:
            Response: A list of jobs.
        """
        params = {
            "uses_category": uses_category,
            "exact": "true" if exact else "false",
            **kwargs,
        }
        return self._get(**params)

    def search_advanced(
        self, filters: List[Dict[str, Any]], limit: Optional[int] = None
    ) -> Response:
        """
        Performs advanced job search using filters via the SourceStack API.

        Args:
            filters: List of filter dictionaries. Each filter should contain:
                    - field: The field to filter on
                    - operator: The operator to use
                    - value: The value to filter by
            limit: Optional maximum number of results to return

        Returns:
            Response: A list of jobs matching the filters.
        """
        url = urljoin(self.base_url, "jobs")
        params = {}
        if limit is not None:
            params["limit"] = limit

        response = self.session.post(url, json={"filters": filters}, params=params)
        response.raise_for_status()
        return response.json()

    def _get(self, **kwargs) -> Response:
        url = urljoin(self.base_url, "jobs")
        response = self.session.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()
