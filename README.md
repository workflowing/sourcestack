# SourceStack

[![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/workflowing/sourcestack/blob/main/LICENSE)
[![PyPi](https://img.shields.io/pypi/v/sourcestack)](https://pypi.org/project/sourcestack/)
[![GitHub](https://img.shields.io/badge/github-repo-blue.svg)](https://github.com/workflowing/sourcestack)

## Installation

```bash
pip install sourcestack
```

## Usage

### Basic Usage

```python
from sourcestack.search import SourceStackSearchService

# Initialize the service
service = SourceStackSearchService(api_key="your-api-key")

# Search for jobs
results = service.search_jobs(name="DevOps")
```

### Basic Search Options

You can search jobs using different parameters:

```python
# Search by job name (supports exact matching)
results = service.search_jobs(name="Platform Engineer", exact=True)

# Search by parent company
results = service.search_jobs(parent="Spotify")

# Search by company URL (automatically strips http://, https://, and www.)
results = service.search_jobs(url="company.com")

# Search by product usage (supports exact matching)
results = service.search_jobs(uses_product="Docker", exact=True)

# Search by product category
results = service.search_jobs(uses_category="Container Orchestration")

# Limit results
results = service.search_jobs(name="developer", limit=5)
```

### Advanced Search

For more complex queries, you can use the advanced search functionality:

```python
# Search with multiple filters
filters = [
    {"field": "remote", "operator": "EQUALS", "value": True},
    {"field": "tags_matched", "operator": "CONTAINS_ANY", "value": ["Python"]}
]
results = service.search_jobs_advanced(filters=filters)

# Advanced search with limit
results = service.search_jobs_advanced(filters=filters, limit=5)

# Date-based filtering
filters = [
    {"field": "last_indexed", "operator": "GREATER_THAN", "value": "LAST_7D"}
]
results = service.search_jobs_advanced(filters=filters)
```

### Search Results

The search results are returned in the following format:

```python
{
    "status": "success",
    "timestamp": "2023-...",  # ISO format timestamp
    "count": int,
    "statistics": {
        "companies": [
            {"name": str, "count": int}
            # Top 5 most common companies
        ],
        "technologies": [
            {"name": str, "count": int}
            # Top 5 most common technologies
        ],
        "categories": [
            {"name": str, "count": int}
            # Top 5 most common categories
        ]
    },
    "entries": [
        {
            "job_name": str,
            "company_name": str,
            "company_url": str,
            "tags_matched": List[str],
            "tag_categories": List[str],
            "remote": bool,
            "country": str,
            # ... other job fields
        }
    ],
    "pagination": {  # Only present when limit is specified
        "limit": int,
        "total": int
    }
}
```

### Important Notes

- Only one search parameter can be used at a time in basic search
- The `exact` parameter can only be used with `name` and `uses_product` searches
- All searches are case-insensitive
- Company URLs are automatically processed to remove common prefixes (http://, https://, www.)
- Advanced search requires at least one filter
- Advanced search filters must contain `field`, `operator`, and `value` keys

## Contributing

For development, install the package with development dependencies:

```bash
pip install -e ".[dev]"
```

### Building

```bash
bin/build
```

### Publishing

```bash
bin/publish
```
