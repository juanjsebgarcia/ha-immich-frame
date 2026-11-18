"""Media player platform for Immich Frame."""

from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ImmichFrameCoordinator
from .entity import ImmichFrameEntity, get_coordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Immich Frame slideshow entity."""
    async_add_entities([ImmichFrameSlideshow(get_coordinator(hass, config_entry), config_entry)])


class ImmichFrameSlideshow(ImmichFrameEntity, MediaPlayerEntity):
    """
    The frame's slideshow, as a media player.

    This gives play, pause, next and previous the standard media controls. The frame only
    has a pause toggle, so play and pause are sent only when they would change something.
    """

    _attr_supported_features = (
        MediaPlayerEntityFeature.NEXT_TRACK
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.PREVIOUS_TRACK
    )

    def __init__(self, coordinator: ImmichFrameCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            name="Slideshow",
            key="slideshow",
        )
        self._assumed_paused = False
        # Set after a toggle and shown until the frame's next report confirms it
        self._pending_paused: bool | None = None

    @callback
    def _handle_coordinator_update(self) -> None:
        self._pending_paused = None
        super()._handle_coordinator_update()

    @property
    def _reported_paused(self) -> bool | None:
        """Return the frame's own paused flag, or None when it does not report one."""
        status = self.status
        if not status:
            return None
        paused = status.get("paused")
        return paused if isinstance(paused, bool) else None

    @property
    def assumed_state(self) -> bool:
        return self._reported_paused is None

    @property
    def state(self) -> MediaPlayerState:
        status = self.status
        if status and status.get("active") is False:
            return MediaPlayerState.OFF

        paused = self._pending_paused
        if paused is None:
            paused = self._reported_paused
        if paused is None:
            paused = self._assumed_paused
        return MediaPlayerState.PAUSED if paused else MediaPlayerState.PLAYING

    async def _async_toggle_pause(self) -> None:
        was_paused = self.state == MediaPlayerState.PAUSED
        await self._async_send_command("pause")
        self._assumed_paused = not was_paused
        self._pending_paused = not was_paused
        self.async_write_ha_state()

    async def async_media_play(self) -> None:
        """Resume the slideshow, unless it is already running or the frame is off."""
        if self.state == MediaPlayerState.PAUSED:
            await self._async_toggle_pause()

    async def async_media_pause(self) -> None:
        """Pause the slideshow, unless it is already paused or the frame is off."""
        if self.state == MediaPlayerState.PLAYING:
            await self._async_toggle_pause()

    async def async_media_next_track(self) -> None:
        """Show the next photo."""
        await self._async_send_command("next")

    async def async_media_previous_track(self) -> None:
        """Show the previous photo."""
        await self._async_send_command("previous")
