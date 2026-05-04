import os
import time
from collections import deque
from api_service import APIService


class DealsService(APIService):
    """
    Service for interacting with HubSpot Deals API, with built-in rate limit handling.
    """

    def __init__(self, access_token):
        super().__init__(base_url="https://api.hubapi.com")
        self.request_timeout = int(os.environ.get("HUBSPOT_API_TIMEOUT", 10))
        self.max_requests = int(os.environ.get("HUBSPOT_API_RATE_LIMIT", 150))
        self.access_token = access_token
        self._request_times = deque()

    """
    Rate limit handling: Track request timestamps and sleep if the limit is reached.
    """
    def _wait_for_rate_limit(self):
        now = time.monotonic()
        window = 10.0
        while self._request_times and self._request_times[0] < now - window:
            self._request_times.popleft()
        if len(self._request_times) >= self.max_requests:
            sleep_for = window - (now - self._request_times[0])
            self.logger.info(f"Rate limit reached, sleeping {sleep_for:.2f}s")
            time.sleep(sleep_for)
        self._request_times.append(time.monotonic())

    def get_deals(self, limit=100, after=None):
        """
        Get deals with pagination support.
            Params:
                limit: Number of records to fetch per request (default: 100)
                after: Cursor for pagination (default: None)
            Returns:
                API response containing deals data
        """
        self._wait_for_rate_limit()
        return self.get_data(self.access_token, limit, after)

    def fetch_all_deals(self):
        """
        Get all deals by handling pagination until no more pages are available.
            Returns:
                List of all deals retrieved from the API
        """
        all_deals = []
        after = None
        while True:
            data = self.get_deals(after=after)
            all_deals.extend(data.get("results", []))
            next_page = data.get("paging", {}).get("next")
            if not next_page:
                break
            after = next_page.get("after")
        return all_deals

    def validate_credentials(self):
        """
        Validate the access token by making a test API call.
             Returns:
                True if the token is valid, False otherwise
        """
        return self.validate_token(self.access_token)