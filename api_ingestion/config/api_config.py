from pathlib import Path


# ---------------------------------------------------------------------------
# API configuration
# ---------------------------------------------------------------------------

API_BASE_URL = "https://dummyjson.com"

CARTS_ENDPOINT = f"{API_BASE_URL}/carts"

DEFAULT_PAGE_SIZE = 10

DEFAULT_TIMEOUT_SECONDS = 30

DEFAULT_MAX_RETRIES = 3

DEFAULT_BACKOFF_FACTOR = 1


# ---------------------------------------------------------------------------
# Landing configuration
# ---------------------------------------------------------------------------

LANDING_ROOT = Path("output/landing")

LANDING_SOURCE_NAME = "sales_api"

LANDING_DATA_ENTITY = "carts"