import os

from dotenv import load_dotenv
from algoliasearch.search_client import SearchClient


load_dotenv()

ALGOLIA_APP_ID = os.environ["ALGOLIA_APP_ID"]
ALGOLIA_API_KEY = os.environ["ALGOLIA_API_KEY"]

algolia_client = SearchClient.create(
    ALGOLIA_APP_ID,
    ALGOLIA_API_KEY,
)


def get_items(search_query: str):
    index = algolia_client.init_index("zara_products")
    results = index.search(
        search_query,
        {
            "page": 1,
            "hitsPerPage": 12,
        },
    )
    return results["hits"]
