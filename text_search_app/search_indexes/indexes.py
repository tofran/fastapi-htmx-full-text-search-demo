from enum import StrEnum

from text_search_app.models import Product
from text_search_app.search_indexes import algolia_index, sqlite_index


class SearchIndex(StrEnum):
    ALGOLIA = "ALGOLIA"
    SQLITE = "SQLITE"


def get_items(
    search_index: SearchIndex = SearchIndex.SQLITE,
    search_query: str | None = None,
) -> list[Product] | None:
    """
    Given a search query returns matching items.
    Returns None if the index is not yet initialized.
    """
    search_func = (
        algolia_index.get_items  # fmt: skip
        if search_index == SearchIndex.ALGOLIA
        else sqlite_index.get_items
    )

    return search_func(search_query)


def load_products_into_index(products: list[Product]):
    """
    Loads the provided products into the index, replacing existing ones.
    This is a destructive action.
    """
    sqlite_index.load_products_into_index(products)
    algolia_index.load_products_into_index(products)
