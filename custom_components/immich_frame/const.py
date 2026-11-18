from homeassistant.const import CONF_HOST

DOMAIN = "immich_frame"
PLATFORMS = ["binary_sensor", "button", "light", "media_player", "sensor"]
DEFAULT_PORT = 53287
COMMAND_TIMEOUT = 10

BRIGHTNESS_COMMAND = "brightness"

# A negative brightness hands the display back to the device's own setting
SYSTEM_BRIGHTNESS_QUERY = "value=-1"
EFFECT_SYSTEM_BRIGHTNESS = "System brightness"

# key, name, enabled by default.
# The slideshow buttons are superseded by the media player entity. They stay for existing
# installs and automations, but are no longer enabled on a new install.
BUTTON_COMMANDS = (
    ("next", "Next photo", False),
    ("previous", "Previous photo", False),
    ("pause", "Pause slideshow", False),
    ("settings", "Open settings", True),
)
STATUS_COMMAND = "status"

# The frame answers a command before it has taken effect
STATUS_REFRESH_DELAY = 1.5

COORDINATOR = "coordinator"
