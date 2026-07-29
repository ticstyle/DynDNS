# const.py
"""Constants for the DynDNS integration."""

from typing import Final

DOMAIN: Final = "dyndns"

CONF_SERVER: Final = "server"
CONF_HOSTNAME: Final = "hostname"
CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"

DEFAULT_SERVER: Final = "test.domain.com"
UPDATE_INTERVAL_MINUTES: Final = 15
