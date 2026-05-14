from __future__ import annotations

import os
from dataclasses import dataclass, field

from deapi._constants import PREFIXES
from deapi._version import __version__

_DEFAULT_BASE_URL = "https://api.deapi.ai"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_API_VERSION = "v2"


@dataclass(frozen=True)
class ClientConfig:
    api_key: str
    base_url: str = _DEFAULT_BASE_URL
    timeout: float = _DEFAULT_TIMEOUT
    max_retries: int = _DEFAULT_MAX_RETRIES
    api_version: str = _DEFAULT_API_VERSION
    _user_agent: str = field(init=False, default=f"deapi-python-sdk/{__version__}")

    @classmethod
    def from_env(
        cls,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        api_version: str | None = None,
    ) -> ClientConfig:
        resolved_key = (api_key or os.environ.get("DEAPI_API_KEY", "")).strip()
        if not resolved_key:
            raise ValueError(
                "API key is required. Pass api_key= or set the DEAPI_API_KEY environment variable."
            )
        return cls(
            api_key=resolved_key,
            base_url=base_url or os.environ.get("DEAPI_BASE_URL", _DEFAULT_BASE_URL),
            timeout=timeout if timeout is not None else _DEFAULT_TIMEOUT,
            max_retries=max_retries if max_retries is not None else _DEFAULT_MAX_RETRIES,
            api_version=api_version or os.environ.get("DEAPI_API_VERSION", _DEFAULT_API_VERSION),
        )

    @property
    def api_prefix(self) -> str:
        # v1: /api/v1/client, v2: /api/v2 (no /client/ segment).
        # Falls back to /api/{version}/client for unknown versions so a future
        # v3 with the same shape works without a code change here.
        return PREFIXES.get(self.api_version, f"/api/{self.api_version}/client")
