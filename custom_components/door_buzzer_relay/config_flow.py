"""Config flow for Door Buzzer Relay integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_SERIAL_PORT,
    CONF_BUZZ_IN_DURATION,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERIAL_PORT): str,
        vol.Required(CONF_BUZZ_IN_DURATION): vol.Coerce(float),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Door Buzzer Relay."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            config = {
                CONF_SERIAL_PORT: user_input[CONF_SERIAL_PORT],
                CONF_BUZZ_IN_DURATION: user_input[CONF_BUZZ_IN_DURATION],
            }

            await self.async_set_unique_id("door_buzzer_relay")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Door Buzzer Relay", 
                data=config,
                description=config[CONF_SERIAL_PORT]
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA
        )
