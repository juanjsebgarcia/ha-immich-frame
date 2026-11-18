from homeassistant.const import CONF_HOST

DOMAIN = "immich_frame"
PLATFORMS = ["binary_sensor", "button", "light", "sensor"]
DEFAULT_PORT = 53287
COMMAND_TIMEOUT = 10

BRIGHTNESS_COMMAND = "brightness"

# key, name, command, query
BUTTON_COMMANDS = (
    ("next", "Next photo", "next", None),
    ("previous", "Previous photo", "previous", None),
    ("pause", "Pause slideshow", "pause", None),
    ("settings", "Open settings", "settings", None),
    # A negative value hands brightness back to the device's own setting
    ("system_brightness", "Use system brightness", BRIGHTNESS_COMMAND, "value=-1"),
)
STATUS_COMMAND = "status"

# The frame answers a command before it has taken effect
STATUS_REFRESH_DELAY = 1.5

COORDINATOR = "coordinator"
