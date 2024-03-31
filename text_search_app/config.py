import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()


def get_bool_env(name: str, default: bool) -> bool:
    return getenv(name, str(default)).lower() == "true"


DEVELOPMENT_MODE = get_bool_env("DEVELOPMENT_MODE", False)
ENABLE_INDEX_MANAGEMENT = get_bool_env("ENABLE_INDEX_MANAGEMENT", True)
PREVENT_HTML_API_DIRECT_ACCESS = get_bool_env(
    "PREVENT_HTML_API_DIRECT_ACCESS", not DEVELOPMENT_MODE
)

ALGOLIA_APP_ID = os.environ["ALGOLIA_APP_ID"]
ALGOLIA_API_KEY = os.environ["ALGOLIA_API_KEY"]
ALGOLIA_INDEX_NAME = os.environ["ALGOLIA_INDEX_NAME"]

SQLITE_DATABASE_PATH = getenv("SQLITE_DATABASE_PATH", "products.sqlite")

RESULTS_PAGE_SIZE = 8
