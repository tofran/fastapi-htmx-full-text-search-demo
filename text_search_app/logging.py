import logging

import text_search_app

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s (%(pathname)s:%(lineno)d)",
)

logger = logging.getLogger(text_search_app.__name__)
