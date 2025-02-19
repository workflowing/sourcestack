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

### Search Options

You can search jobs using different parameters:

```python
# Search by job name (supports exact matching)
results = service.search_jobs(name="Platform Engineer", exact=True)

# Search by parent company
results = service.search_jobs(parent="Spotify")

# Search by company URL
results = service.search_jobs(url="company.com")

# Search by product usage (supports exact matching)
results = service.search_jobs(uses_product="Docker", exact=True)

# Search by product category
results = service.search_jobs(uses_category="Container Orchestration")

# Limit results
results = service.search_jobs(name="developer", limit=5)
```

### Search Results

The search results are returned in the following format:

```python
{
    "status": "success",
    "count": int,
    "entries": [
        {
            "job_name": str,
            "company_name": str,
            "company_url": str,
            "tags_matched": List[str],
            "tag_categories": List[str]
        }
    ],
    "pagination": {
        "limit": int
    }
}
```

### Important Notes

- Only one search parameter can be used at a time
- The `exact` parameter can only be used with `name` and `uses_product` searches
- All searches are case-insensitive

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
