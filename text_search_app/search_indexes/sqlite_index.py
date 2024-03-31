"""
One could use SQLAlchemy in a production environment,
but here, for simplicity and readability of SQL queries I used the standard, sqlite3 module.
Noe that it is sync, meaning that it is thread blocking
"""

import sqlite3

from text_search_app.config import RESULTS_PAGE_SIZE, SQLITE_DATABASE_PATH
from text_search_app.logging import logger
from text_search_app.models import Product

sqlite_connection = sqlite3.connect(SQLITE_DATABASE_PATH)

sqlite_connection.row_factory = sqlite3.Row


def setup_db() -> None:
    sqlite_connection.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS products USING fts5 (
            sku,
            name,
            description,
            price,
            currency,
            terms,
            section,
            tokenize="porter unicode61"
        )
        """
    )

    logger.info("Database setup complete")


def is_db_initialized() -> bool:
    try:
        sqlite_connection.execute("SELECT * FROM products LIMIT 1")
        return True
    except sqlite3.OperationalError:
        return False


def load_products_into_index(products: list[Product]) -> None:
    with sqlite_connection:
        sqlite_connection.execute("DELETE FROM products")

        sqlite_connection.executemany(
            """
            INSERT INTO products (sku, name, description, price, currency, terms, section)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                (
                    product.sku,
                    product.name,
                    product.description,
                    product.price,
                    product.currency,
                    product.terms,
                    product.section,
                )
                for product in products
            ),
        )

    logger.info(
        f"Successfully replaced products SQLite database with {len(products)} items",
    )


def get_items(
    search_query: str | None = None,
) -> list[Product] | None:
    if not is_db_initialized():
        return None

    if search_query:
        query = sqlite_connection.execute(
            """
            SELECT *
            FROM products
            WHERE products MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (search_query, RESULTS_PAGE_SIZE),
        )
    else:
        query = sqlite_connection.execute(
            """
            SELECT *
            FROM products
            LIMIT ?
            """,
            (RESULTS_PAGE_SIZE,),
        )

    result = query.fetchall()

    logger.info(
        f"SQLite search returned {len(result)!r} item for search_query={search_query!r}",
    )

    return [
        Product.model_validate(dict(product_result))  # fmt: skip
        for product_result in result
    ]
