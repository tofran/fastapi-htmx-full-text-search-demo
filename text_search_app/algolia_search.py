from typing import Any

from algoliasearch.search_client import SearchClient

from text_search_app.config import ALGOLIA_API_KEY, ALGOLIA_APP_ID

algolia_client = SearchClient.create(
    ALGOLIA_APP_ID,
    ALGOLIA_API_KEY,
)


def get_items(search_query: str) -> Any:
    index = algolia_client.init_index("zara_products")
    results = index.search(
        search_query,
        {
            "page": 1,
            "hitsPerPage": 12,
        },
    )
    return results["hits"]
