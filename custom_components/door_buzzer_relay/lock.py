from __future__ import annotations

from typing import Any

from homeassistant.components.lock import (
    LockEntity,
    LockEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_LOCKED, STATE_UNLOCKED
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .buzzer import Buzzer
from .const import DOMAIN, CONF_BUZZ_IN_DURATION

import asyncio

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    buzzer = hass.data[DOMAIN][config_entry.entry_id]
    config = config_entry.data
    entities = [BuzzerLock(buzzer, config)]
    async_add_entities(entities, True)


class BuzzerLock(LockEntity):
    def __init__(self, buzzer: Buzzer, config) -> None:
        self._attr_supported_features = LockEntityFeature.OPEN
        self._attr_unique_id = "buzzer_door"
        self._buzzer = buzzer
        self._config = config
        self._state = STATE_LOCKED
        self._release_task = None

    async def async_unlock(self, **kwargs: Any) -> None:
        self._cancel_release_task()
        
        self._buzzer.press()
        self._state = STATE_UNLOCKED        
        await self.async_update_ha_state()

        self._release_task = asyncio.create_task(self._release_after_delay())

    async def async_lock(self, **kwargs: Any) -> None:
        self._cancel_release_task()

        await self._release()

    async def _release_after_delay(self) -> None:
        await asyncio.sleep(self._config[CONF_BUZZ_IN_DURATION])
        await self._release()
        
    async def _release(self) -> None:
        self._buzzer.release()
        self._state = STATE_LOCKED
        await self.async_update_ha_state()

    async def _cancel_release_task(self) -> None:
        if self._release_task is not None and not self._release_task.done:
            self._release_task.cancel()
            self._release_task = None

    @property
    def is_unlocking(self) -> bool | None:
        return False

    @property
    def is_unlocked(self) -> bool | None:
        return self._state == STATE_UNLOCKED

    @property
    def is_locking(self) -> bool | None:
        return False

    @property
    def is_locked(self) -> bool | None:
        return self._state == STATE_LOCKED
