"""Minimal client for the Duecanali /am JSON endpoint."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

from .const import CLIENT_ID

_LOGGER = logging.getLogger(__name__)


class DuecanaliError(Exception):
    """Communication or protocol error."""


class DuecanaliClient:
    def __init__(self, session: aiohttp.ClientSession, host: str) -> None:
        self._session = session
        self._url = f"http://{host}/am"

    async def _request(self, action_type: str, value: dict[str, Any]) -> dict[str, Any]:
        body = {
            "clientId": CLIENT_ID,
            "payload": {
                "type": "ACTION",
                "action": {"type": action_type, "values": [value]},
            },
        }
        try:
            async with asyncio.timeout(10):
                resp = await self._session.post(self._url, json=body)
                resp.raise_for_status()
                data = await resp.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError) as err:
            raise DuecanaliError(f"Cannot reach amp: {err}") from err

        try:
            return data["payload"]["action"]["values"][0]
        except (KeyError, IndexError, TypeError) as err:
            raise DuecanaliError(f"Unexpected response: {data}") from err

    async def read_data(self, path: str) -> dict[str, Any]:
        item = await self._request("READ", {"id": path, "single": True})
        data = item.get("data")
        if not isinstance(data, dict):
            raise DuecanaliError(f"No data in response for {path}: {item}")
        return data

    async def read_bool(self, path: str) -> bool:
        data = await self.read_data(path)
        if "boolValue" not in data:
            raise DuecanaliError(f"No boolValue for {path}: {data}")
        return bool(data["boolValue"])

    async def read_raw_value(self, path: str) -> Any:
        """Return the first value field of the data object (not 'type')."""
        data = await self.read_data(path)
        for key, val in data.items():
            if key != "type":
                return val
        return None

    async def write_bool(self, path: str, value: bool) -> None:
        item = await self._request(
            "WRITE",
            {"id": path, "data": {"type": "BOOL", "boolValue": value}},
        )
        if item.get("result") != 10:
            _LOGGER.warning("Write to %s returned result %s", path, item.get("result"))
