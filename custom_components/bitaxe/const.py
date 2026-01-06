"""Constants for the Bitaxe integration."""
from homeassistant.const import Platform

DOMAIN = "bitaxe"

# Platforms
PLATFORMS = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.BUTTON,
    Platform.NUMBER,
]

# Configuration
CONF_IP = "host"
CONF_NAME = "name"
CONF_PORT = "port"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_PORT = 80
DEFAULT_SCAN_INTERVAL = 15  # seconds

# API Endpoints
API_SYSTEM_INFO = "/api/system/info"
API_SYSTEM_ASIC = "/api/system/asic"
API_SYSTEM_RESTART = "/api/system/restart"
API_SYSTEM_IDENTIFY = "/api/system/identify"
API_SYSTEM_UPDATE = "/api/system"

# Units
GIGA_HASH_PER_SECOND = "GH/s"

# Overheat modes
OVERHEAT_MODE_DISABLED = 0

OVERHEAT_MODES = {
    "Disabled": OVERHEAT_MODE_DISABLED,
}

# Screen rotation options
ROTATION_0 = 0
ROTATION_90 = 90
ROTATION_180 = 180
ROTATION_270 = 270

ROTATION_OPTIONS = {
    "0°": ROTATION_0,
    "90°": ROTATION_90,
    "180°": ROTATION_180,
    "270°": ROTATION_270,
}

# Default data structure for when device is unavailable
DEFAULT_DATA = {
    "ASICModel": "Unknown",
    "macAddr": "00:00:00:00:00:00",
    "hostname": "bitaxe",
    "ipv4": "0.0.0.0",
    "temp": 0,
    "vrTemp": 0,
    "hashRate": 0,
    "power": 0,
    "voltage": 0,
    "current": 0,
    "fanspeed": 0,
    "fanrpm": 0,
    "sharesAccepted": 0,
    "sharesRejected": 0,
    "uptimeSeconds": 0,
    "wifiRSSI": 0,
    "freeHeap": 0,
    "coreVoltage": 1200,
    "frequency": 500,
}
