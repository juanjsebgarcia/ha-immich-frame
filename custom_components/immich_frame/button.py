"""Button platform for Immich Frame."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BUTTON_COMMANDS, DOMAIN
from .coordinator import ImmichFrameCoordinator
from .entity import ImmichFrameEntity, get_coordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities for Immich Frame."""
    coordinator = get_coordinator(hass, config_entry)
    async_add_entities(
        ImmichFrameButton(
            coordinator=coordinator,
            config_entry=config_entry,
            description=ButtonEntityDescription(key=key, name=name),
            command=command,
            query=query,
        )
        for key, name, command, query in BUTTON_COMMANDS
    )


class ImmichFrameButton(ImmichFrameEntity, ButtonEntity):
    """Immich Frame button entity."""

    entity_description: ButtonEntityDescription

    def __init__(
        self,
        coordinator: ImmichFrameCoordinator,
        config_entry: ConfigEntry,
        description: ButtonEntityDescription,
        command: str,
        query: str | None,
    ) -> None:
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            name=description.name,
            key=description.key,
        )
        self.entity_description = description
        self._command = command
        self._query = query

    async def async_press(self) -> None:
        """Send the configured command to the Immich Frame."""
        await self._async_send_command(self._command, self._query)
