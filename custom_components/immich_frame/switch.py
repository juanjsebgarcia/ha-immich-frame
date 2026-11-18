"""Switch platform for Immich Frame."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ImmichFrameCoordinator
from .entity import ImmichFrameEntity, get_coordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the image adjustments switch for frames that report adjustments."""
    coordinator = get_coordinator(hass, config_entry)
    if not coordinator.data or "adjustments" not in coordinator.data:
        return

    async_add_entities([ImmichFrameAdjustmentsSwitch(coordinator, config_entry)])


class ImmichFrameAdjustmentsSwitch(ImmichFrameEntity, SwitchEntity):
    """Turns the frame's image adjustments on and off as a whole."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: ImmichFrameCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            name="Image adjustments",
            key="adjustments_enabled",
        )

    @property
    def is_on(self) -> bool | None:
        enabled = self.adjustments.get("enabled")
        return enabled if isinstance(enabled, bool) else None

    async def async_turn_on(self, **kwargs) -> None:
        """Apply the adjustments to the picture."""
        await self._async_set_adjustments("enabled=true", {"enabled": True})

    async def async_turn_off(self, **kwargs) -> None:
        """Show the picture unadjusted, keeping the values for later."""
        await self._async_set_adjustments("enabled=false", {"enabled": False})
