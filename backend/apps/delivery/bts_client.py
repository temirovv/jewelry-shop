import logging
import time

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 15
MAX_RETRIES = 2
RETRY_DELAY = 1  # seconds


class BTSAPIError(Exception):
    """BTS API bilan bog'liq xatolik."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class BTSClient:
    """BTS Express API Client with token caching and retry."""

    TOKEN_TTL = 24 * 60 * 60  # 24 hours

    def __init__(self):
        self.base_url = settings.BTS_API_URL
        self.username = settings.BTS_USERNAME
        self.password = settings.BTS_PASSWORD
        self._token: str | None = None
        self._token_expires: float = 0

    @property
    def token(self) -> str:
        if self._token and time.time() < self._token_expires:
            return self._token
        self.authenticate()
        return self._token  # type: ignore[return-value]

    def authenticate(self):
        """POST /auth/login — authenticate and cache token."""
        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT, verify=False) as client:
                response = client.post(
                    f"{self.base_url}/auth/login",
                    json={
                        "username": self.username,
                        "password": self.password,
                    },
                )
                response.raise_for_status()
                data = response.json()
                self._token = data.get("token") or data.get("access_token")
                if not self._token:
                    raise BTSAPIError("BTS auth response'da token topilmadi")
                self._token_expires = time.time() + self.TOKEN_TTL
                logger.info("BTS authentication successful")
        except httpx.TimeoutException:
            logger.error("BTS authentication timeout")
            raise BTSAPIError("BTS server javob bermadi (timeout)")
        except httpx.HTTPStatusError as e:
            logger.error(f"BTS authentication failed: {e.response.status_code}")
            raise BTSAPIError(f"BTS auth xatolik: {e.response.status_code}", e.response.status_code)
        except httpx.HTTPError as e:
            logger.error(f"BTS authentication failed: {e}")
            raise BTSAPIError(f"BTS ulanish xatolik: {e}")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Generic request with auto-auth retry and retries on failure."""
        url = f"{self.base_url}{path}"
        last_error = None

        for attempt in range(MAX_RETRIES + 1):
            try:
                with httpx.Client(timeout=REQUEST_TIMEOUT, verify=False) as client:
                    response = getattr(client, method)(
                        url, headers=self._headers(), **kwargs
                    )
                    if response.status_code == 401:
                        self.authenticate()
                        response = getattr(client, method)(
                            url, headers=self._headers(), **kwargs
                        )
                    response.raise_for_status()
                    return response.json()
            except httpx.TimeoutException:
                last_error = BTSAPIError(f"BTS timeout [{method.upper()} {path}]")
                logger.warning(f"BTS timeout [{method.upper()} {path}], attempt {attempt + 1}/{MAX_RETRIES + 1}")
            except httpx.HTTPStatusError as e:
                last_error = BTSAPIError(
                    f"BTS xatolik [{method.upper()} {path}]: {e.response.status_code}",
                    e.response.status_code,
                )
                # 4xx xatoliklar uchun retry qilmaymiz (client error)
                if 400 <= e.response.status_code < 500:
                    raise last_error
                logger.warning(f"BTS server error [{method.upper()} {path}]: {e.response.status_code}, attempt {attempt + 1}")
            except httpx.HTTPError as e:
                last_error = BTSAPIError(f"BTS ulanish xatolik: {e}")
                logger.warning(f"BTS connection error [{method.upper()} {path}], attempt {attempt + 1}")

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (attempt + 1))

        raise last_error  # type: ignore[misc]

    def calculate_delivery(
        self,
        sender_region: int,
        receiver_region: int,
        receiver_city: int,
        weight: float = 0.5,
    ) -> dict:
        """POST /order/calculator — calculate delivery cost."""
        return self._request(
            "post",
            "/order/calculator",
            json={
                "sender_region_id": sender_region,
                "receiver_region_id": receiver_region,
                "receiver_city_id": receiver_city,
                "weight": weight,
            },
        )

    def create_order(self, order_data: dict) -> dict:
        """POST /order/add — create a shipment."""
        return self._request("post", "/order/add", json=order_data)

    def get_tracking(self, shipment_id: str) -> dict:
        """GET /tracking — get shipment tracking info."""
        return self._request("get", f"/tracking?shipment_id={shipment_id}")

    def cancel_order(self, shipment_id: str) -> dict:
        """POST /order/cancel — cancel a shipment."""
        return self._request("post", "/order/cancel", json={"shipment_id": shipment_id})

    def get_regions(self) -> list:
        """GET /directory/regions — list all regions."""
        data = self._request("get", "/directory/regions")
        return data if isinstance(data, list) else data.get("data", data.get("results", []))

    def get_cities(self, region_id: int) -> list:
        """GET /directory/cities — list cities in a region."""
        data = self._request("get", f"/directory/cities?region_id={region_id}")
        return data if isinstance(data, list) else data.get("data", data.get("results", []))


# Singleton instance
_client: BTSClient | None = None


def get_bts_client() -> BTSClient:
    global _client
    if _client is None:
        _client = BTSClient()
    return _client
