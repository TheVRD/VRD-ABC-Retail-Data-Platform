import time

import requests


class DummyJsonAPIError(Exception):
    """Raised when DummyJSON returns an API-related error."""

    pass


class DummyJsonClient:
    """
    Client responsible for communicating with the DummyJSON API.
    """

    RETRYABLE_STATUS_CODES = {
        429,
        500,
        502,
        503,
        504,
    }

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: int = 1,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        self.session = requests.Session()

    def fetch_carts_page(
        self,
        *,
        skip: int,
        limit: int,
    ) -> dict:
        """
        Fetch one page of carts from DummyJSON.

        Retries transient HTTP failures using exponential backoff.

        Parameters
        ----------
        skip : int
            Number of records to skip.

        limit : int
            Maximum number of records to return.

        Returns
        -------
        dict
            Complete JSON response from DummyJSON.

        Raises
        ------
        DummyJsonAPIError
            If the API request ultimately fails.
        """

        endpoint = f"{self.base_url}/carts"

        params = {
            "skip": skip,
            "limit": limit,
        }

        for attempt in range(self.max_retries + 1):

            try:
                response = self.session.get(
                    endpoint,
                    params=params,
                    timeout=self.timeout,
                )

                if response.status_code in self.RETRYABLE_STATUS_CODES:

                    if attempt < self.max_retries:

                        self._wait_before_retry(attempt)

                        continue

                    raise DummyJsonAPIError(
                        f"API request failed after "
                        f"{self.max_retries} retries. "
                        f"status_code={response.status_code}, "
                        f"skip={skip}, "
                        f"limit={limit}"
                    )

                response.raise_for_status()

                try:
                    return response.json()

                except ValueError as exc:
                    raise DummyJsonAPIError(
                        "API returned an invalid JSON response."
                    ) from exc

            except requests.exceptions.Timeout as exc:

                if attempt < self.max_retries:

                    self._wait_before_retry(attempt)

                    continue

                raise DummyJsonAPIError(
                    f"Request timed out after "
                    f"{self.max_retries} retries. "
                    f"skip={skip}, "
                    f"limit={limit}"
                ) from exc

            except requests.exceptions.RequestException as exc:

                raise DummyJsonAPIError(
                    f"Request failed. "
                    f"skip={skip}, "
                    f"limit={limit}"
                ) from exc

        raise DummyJsonAPIError(
            f"Request failed unexpectedly. "
            f"skip={skip}, "
            f"limit={limit}"
        )

    def _wait_before_retry(self, attempt: int) -> None:
        """
        Wait using exponential backoff before retrying.
        """

        delay = self.backoff_factor * (2 ** attempt)

        print(
            f"Transient API failure. "
            f"Retrying in {delay} seconds..."
        )

        time.sleep(delay)

    def close(self) -> None:
        """Close the underlying HTTP session."""

        self.session.close()