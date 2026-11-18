"""Number platform for Immich Frame."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ImmichFrameCoordinator
from .entity import ImmichFrameEntity, get_coordinator

# Keyed by the adjustment's name in the frame's API. The ranges are the app's own.
# "Image brightness" is the picture's brightness, as distinct from the display's backlight,
# which is the light entity.
ADJUSTMENTS = (
    NumberEntityDescription(
        key="brightness",
        name="Image brightness",
        native_min_value=-50,
        native_max_value=50,
        native_step=1,
    ),
    NumberEntityDescription(
        key="contrast",
        name="Image contrast",
        native_min_value=-50,
        native_max_value=50,
        native_step=1,
    ),
    NumberEntityDescription(
        key="red",
        name="Image red",
        native_min_value=-50,
        native_max_value=50,
        native_step=1,
    ),
    NumberEntityDescription(
        key="green",
        name="Image green",
        native_min_value=-50,
        native_max_value=50,
        native_step=1,
    ),
    NumberEntityDescription(
        key="blue",
        name="Image blue",
        native_min_value=-50,
        native_max_value=50,
        native_step=1,
    ),
    NumberEntityDescription(
        key="gamma",
        name="Image gamma",
        native_min_value=0.1,
        native_max_value=2.0,
        native_step=0.01,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the image adjustment sliders for frames that report adjustments."""
    coordinator = get_coordinator(hass, config_entry)
    if not coordinator.data or "adjustments" not in coordinator.data:
        return

    async_add_entities(
        ImmichFrameAdjustment(coordinator, config_entry, description)
        for description in ADJUSTMENTS
    )


class ImmichFrameAdjustment(ImmichFrameEntity, NumberEntity):
    """One of the frame's image adjustments."""

    entity_description: NumberEntityDescription
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.SLIDER

    def __init__(
        self,
        coordinator: ImmichFrameCoordinator,
        config_entry: ConfigEntry,
        description: NumberEntityDescription,
    ) -> None:
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            name=description.name,
            key=f"adjustment_{description.key}",
        )
        self.entity_description = description

    @property
    def native_value(self) -> float | None:
        value = self.adjustments.get(self.entity_description.key)
        return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None

    async def async_set_native_value(self, value: float) -> None:
        """Send the new value to the frame, which applies it to the picture at once."""
        key = self.entity_description.key
        if key == "gamma":
            sent: float = round(value, 2)
            query = f"{key}={sent:.2f}"
        else:
            sent = int(round(value))
            query = f"{key}={sent}"
        await self._async_set_adjustments(query, {key: sent})
