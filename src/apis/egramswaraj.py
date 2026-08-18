import asyncio
import logging
import os
import time
from typing import Any

import httpx


logger = logging.getLogger(__name__)


class EGramSwarajUnavailable(RuntimeError):
    """Raised when the eGramSwaraj upstream cannot serve a request."""


class EGramSwarajClient:
    BASE_URL = "https://egramswaraj.gov.in/webservice"
    CACHE_TTL_SECONDS = int(os.getenv("EGRAMSWARAJ_CACHE_TTL_SECONDS", "1800"))
    MAX_ATTEMPTS = 3

    def __init__(self) -> None:
        self._cache: dict[tuple[int, int, int], tuple[float, Any]] = {}
        self._cache_lock = asyncio.Lock()

    async def get_planning_data(
        self,
        state_code: int,
        plan_year: int,
        lgd_code: int,
    ) -> Any:
        cache_key = (state_code, plan_year, lgd_code)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        # A single in-process request prevents a dashboard's concurrent endpoints
        # from repeatedly hitting the government service for the same data.
        async with self._cache_lock:
            cached = self._get_cached(cache_key)
            if cached is not None:
                return cached

            data = await self._fetch_planning_data(
                state_code=state_code,
                plan_year=plan_year,
                lgd_code=lgd_code,
            )
            self._cache[cache_key] = (time.monotonic(), data)
            return data

    def _get_cached(self, cache_key: tuple[int, int, int]) -> Any | None:
        cached = self._cache.get(cache_key)
        if cached is None:
            return None

        cached_at, data = cached
        if time.monotonic() - cached_at < self.CACHE_TTL_SECONDS:
            return data

        del self._cache[cache_key]
        return None

    async def _fetch_planning_data(
        self,
        state_code: int,
        plan_year: int,
        lgd_code: int,
    ) -> Any:
        url = (
            f"{self.BASE_URL}/"
            f"getLbApprovedActivityData/"
            f"{state_code}/{plan_year}/{lgd_code}"
        )
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)
        last_error: Exception | None = None

        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": "udupi-map-backend/1.0"},
        ) as http_client:
            for attempt in range(self.MAX_ATTEMPTS):
                try:
                    response = await http_client.get(url)
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as exc:
                    # Retrying a client error only adds load; a 429/5xx may recover.
                    if exc.response.status_code < 500 and exc.response.status_code != 429:
                        raise EGramSwarajUnavailable(
                            "eGramSwaraj rejected the request."
                        ) from exc
                    last_error = exc
                except httpx.RequestError as exc:
                    last_error = exc

                if attempt < self.MAX_ATTEMPTS - 1:
                    await asyncio.sleep(2**attempt)

        logger.warning("eGramSwaraj request failed after retries: %s", last_error)
        raise EGramSwarajUnavailable(
            "eGramSwaraj is temporarily unavailable."
        ) from last_error


client = EGramSwarajClient()
