from api_ingestion.clients.dummyjson_client import DummyJsonClient
from api_ingestion.config.api_config import (
    API_BASE_URL,
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_MAX_RETRIES,
    DEFAULT_PAGE_SIZE,
    DEFAULT_TIMEOUT_SECONDS,
)


def main():

    client = DummyJsonClient(
        base_url=API_BASE_URL,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        max_retries=DEFAULT_MAX_RETRIES,
        backoff_factor=DEFAULT_BACKOFF_FACTOR,
    )

    try:

        response = client.fetch_carts_page(
            skip=0,
            limit=DEFAULT_PAGE_SIZE,
        )

        print(f"Total carts: {response['total']}")
        print(f"Skip: {response['skip']}")
        print(f"Limit: {response['limit']}")
        print(f"Carts returned: {len(response['carts'])}")

    finally:

        client.close()


if __name__ == "__main__":
    main()