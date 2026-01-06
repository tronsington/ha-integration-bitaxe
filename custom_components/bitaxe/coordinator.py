"""Coordinator for Bitaxe integration."""
from datetime import timedelta
import logging
import asyncio
from typing import Any

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    API_SYSTEM_INFO,
    API_SYSTEM_UPDATE,
    API_SYSTEM_RESTART,
    API_SYSTEM_IDENTIFY,
    DEFAULT_DATA,
)

_LOGGER = logging.getLogger(__name__)


class BitaxeApiClient:
    """API client for Bitaxe device."""

    def __init__(self, host: str, port: int) -> None:
        """Initialize the API client."""
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    async def get_system_info(self) -> dict[str, Any]:
        """Get system information from the device."""
        url = f"{self.base_url}{API_SYSTEM_INFO}"
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()

    async def update_settings(self, settings: dict[str, Any]) -> None:
        """Update device settings."""
        url = f"{self.base_url}{API_SYSTEM_UPDATE}"
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, json=settings) as response:
                    response.raise_for_status()

    async def restart(self) -> None:
        """Restart the device."""
        url = f"{self.base_url}{API_SYSTEM_RESTART}"
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as response:
                    response.raise_for_status()

    async def identify(self) -> None:
        """Trigger device identification."""
        url = f"{self.base_url}{API_SYSTEM_IDENTIFY}"
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as response:
                    response.raise_for_status()


class BitaxeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Bitaxe data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: BitaxeApiClient,
        name: str,
        scan_interval: int,
    ) -> None:
        """Initialize the coordinator."""
        self.api = api
        self.name = name
        self._failure_count = 0

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{name}",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the Bitaxe device."""
        try:
            data = await self.api.get_system_info()
            self._failure_count = 0
            
            # Add IP address to data for device info
            data["ip"] = self.api.host
            
            _LOGGER.debug("Successfully fetched data from %s: %s", self.name, data)
            return data

        except asyncio.TimeoutError as err:
            self._failure_count += 1
            if self._failure_count > 3:
                raise UpdateFailed(f"Timeout connecting to {self.name}") from err
            _LOGGER.warning("Timeout fetching data from %s (attempt %d)", self.name, self._failure_count)
            return DEFAULT_DATA

        except aiohttp.ClientError as err:
            self._failure_count += 1
            if self._failure_count > 3:
                raise UpdateFailed(f"Error connecting to {self.name}: {err}") from err
            _LOGGER.warning("Error fetching data from %s (attempt %d): %s", self.name, self._failure_count, err)
            return DEFAULT_DATA

        except Exception as err:
            self._failure_count += 1
            if self._failure_count > 3:
                raise UpdateFailed(f"Unexpected error from {self.name}: {err}") from err
            _LOGGER.warning("Unexpected error fetching data from %s (attempt %d): %s", self.name, self._failure_count, err)
            return DEFAULT_DATA
