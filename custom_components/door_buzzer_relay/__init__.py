"""The Door Buzzer Relay integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_SERIAL_PORT
from .buzzer import Buzzer

PLATFORMS: list[Platform] = [Platform.LOCK]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Door Buzzer Relay from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = Buzzer(entry.data[CONF_SERIAL_PORT])

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
