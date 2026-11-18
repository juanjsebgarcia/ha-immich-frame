"""Button platform for Immich Frame."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import EntityCategory

from .const import ADJUSTMENTS_COMMAND, BUTTON_COMMANDS, DOMAIN, RELOAD_COMMAND
from .coordinator import ImmichFrameCoordinator
from .entity import ImmichFrameEntity, get_coordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities for Immich Frame."""
    coordinator = get_coordinator(hass, config_entry)
    descriptions = [
        ButtonEntityDescription(
            key=key,
            name=name,
            entity_registry_enabled_default=enabled,
        )
        for key, name, enabled in BUTTON_COMMANDS
    ]
    # Reload arrived in the same build of the app as the media report
    if coordinator.data and "media" in coordinator.data:
        descriptions.append(
            ButtonEntityDescription(
                key=RELOAD_COMMAND,
                name="Reload",
                entity_category=EntityCategory.CONFIG,
            )
        )

    entities: list[ButtonEntity] = [
        ImmichFrameButton(coordinator, config_entry, description)
        for description in descriptions
    ]
    if coordinator.data and "adjustments" in coordinator.data:
        entities.append(ImmichFrameResetAdjustmentsButton(coordinator, config_entry))

    async_add_entities(entities)


class ImmichFrameButton(ImmichFrameEntity, ButtonEntity):
    """Immich Frame button entity."""

    entity_description: ButtonEntityDescription

    def __init__(
        self,
        coordinator: ImmichFrameCoordinator,
        config_entry: ConfigEntry,
        description: ButtonEntityDescription,
    ) -> None:
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            name=description.name,
            key=description.key,
        )
        self.entity_description = description

    async def async_press(self) -> None:
        """Send the configured command to the Immich Frame."""
        await self._async_send_command(self.entity_description.key)


class ImmichFrameResetAdjustmentsButton(ImmichFrameEntity, ButtonEntity):
    """Puts the image adjustments back to their defaults."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: ImmichFrameCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            name="Reset image adjustments",
            key="reset_adjustments",
        )

    async def async_press(self) -> None:
        """Reset every adjustment value, leaving adjustments switched on or off as they were."""
        await self._async_set_adjustments(
            "reset=true",
            {"blue": 0, "brightness": 0, "contrast": 0, "gamma": 1.0, "green": 0, "red": 0},
        )
