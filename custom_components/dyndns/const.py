# const.py
"""Constants for the DynDNS integration."""

from typing import Final

DOMAIN: Final = "dyndns"

CONF_PROTOCOL: Final = "protocol"
CONF_SERVER: Final = "server"
CONF_HOSTNAME: Final = "hostname"
CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"
CONF_UPDATE_INTERVAL: Final = "update_interval"

PROTOCOL_DYNDNS2: Final = "dyndns2"
PROTOCOL_HTTP_GET: Final = "http_get"

SUPPORTED_PROTOCOLS: Final = [PROTOCOL_DYNDNS2, PROTOCOL_HTTP_GET]

DEFAULT_SERVER: Final = "cloud.test.org"
DEFAULT_UPDATE_INTERVAL_MINUTES: Final = 15
