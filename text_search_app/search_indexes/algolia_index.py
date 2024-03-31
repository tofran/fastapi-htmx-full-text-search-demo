from algoliasearch.search_client import SearchClient

from text_search_app.config import (
    ALGOLIA_API_KEY,
    ALGOLIA_APP_ID,
    ALGOLIA_INDEX_NAME,
    RESULTS_PAGE_SIZE,
)
from text_search_app.logging import logger
from text_search_app.models import Product

algolia_client = SearchClient.create(
    ALGOLIA_APP_ID,
    ALGOLIA_API_KEY,
)

algolia_index = algolia_client.init_index(ALGOLIA_INDEX_NAME)


def get_items(search_query: str | None = None) -> list[Product] | None:
    if not algolia_index.exists():
        return None

    results = algolia_index.search(
        search_query,
        {
            "page": 0,
            "hitsPerPage": RESULTS_PAGE_SIZE,
        },
    )

    search_results = results["hits"]

    logger.info(
        f"Algolia search returned {len(search_results)!r} item for search_query={search_query!r}"
    )

    return [
        Product.model_validate(search_result)  # fmt: skip
        for search_result in search_results
    ]


def load_products_into_index(products: list[Product]):
    # TODO: This is thread blocking since it is using Algolia's sync methods, change to async

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
        f"Successfully replaced objects in Algolia index {algolia_index.name!r} "
        f"with {len(products)} items"
    )
