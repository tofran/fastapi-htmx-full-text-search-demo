from algoliasearch.search_client import SearchClient

from text_search_app.config import ALGOLIA_API_KEY, ALGOLIA_APP_ID, ALGOLIA_INDEX_NAME
from text_search_app.logging import logger
from text_search_app.models import AlgoliaSearchResult, Product

algolia_client = SearchClient.create(
    ALGOLIA_APP_ID,
    ALGOLIA_API_KEY,
)

algolia_index = algolia_client.init_index(ALGOLIA_INDEX_NAME)


def get_items(search_query: str) -> list[AlgoliaSearchResult] | None:
    """
    Given a search query returns matching items.
    Returns None if the index is not yet initialized.
    """
    if not algolia_index.exists():
        return None

    results = algolia_index.search(
        search_query,
        {
            "page": 1,
            "hitsPerPage": 12,
        },
    )

    search_results = results["hits"]

    logger.info(
        f"Algolia search returned {len(search_results)!r} item for search_query={search_query!r}"
    )

    return [
        AlgoliaSearchResult.model_validate(search_result)  # fmt: skip
        for search_result in search_results
    ]


def load_products_into_index(products: list[Product]):
    """
    Loads the provided products into the index, replacing existing ones.
    This is a destructive action.
    TODO: This is thread blocking since it is using Algolia's sync methods, change to async
    """
    logger.info(f"Replacing all objects in Algolia {algolia_index.name!r} index")

    algolia_index.replace_all_objects(
        [
            product.model_dump()  # fmt: skip
            for product in products
        ],
        request_options={
            "autoGenerateObjectIDIfNotExist": True,
        },
    )

    logger.info(
        f"Successfully replaced objects in {algolia_index.name!r} with {len(products)} items"
    )
