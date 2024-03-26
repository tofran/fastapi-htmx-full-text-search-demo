import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()

DEVELOPMENT_MODE = getenv("DEVELOPMENT_MODE", "false").lower() == "true"

ALGOLIA_APP_ID = os.environ["ALGOLIA_APP_ID"]
ALGOLIA_API_KEY = os.environ["ALGOLIA_API_KEY"]
