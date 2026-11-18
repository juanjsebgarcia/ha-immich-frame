from homeassistant.const import CONF_HOST

DOMAIN = "immich_frame"
PLATFORMS = ["binary_sensor", "button", "light", "sensor"]
DEFAULT_PORT = 53287
COMMAND_TIMEOUT = 10

BUTTON_COMMANDS = (
    ("next", "Next photo"),
    ("previous", "Previous photo"),
    ("pause", "Pause slideshow")
)

BRIGHTNESS_COMMAND = "brightness"
STATUS_COMMAND = "status"

# The frame answers a command before it has taken effect
STATUS_REFRESH_DELAY = 1.5

COORDINATOR = "coordinator"
