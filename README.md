# DynDNS

![Latest Release](https://img.shields.io/github/release/ticstyle/DynDNS?color=blue&label=Release)
![Last Updated](https://img.shields.io/github/last-commit/ticstyle/DynDNS?path=hacs.json&label=Maintained)
![Issues](https://img.shields.io/github/issues/ticstyle/DynDNS?color=orange&label=Issues)
![Custom Integration](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-blue?logo=home-assistant)
![Home Assistant Required Version](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/ticstyle/DynDNS/main/hacs.json&query=%24.homeassistant&suffix=%2B&label=Home%20Assistant&logo=homeassistant)

![License](https://img.shields.io/github/license/ticstyle/DynDNS?label=License)
[![Hassfest](https://img.shields.io/github/actions/workflow/status/ticstyle/DynDNS/pipeline.yml?branch=main&label=Hassfest)](https://github.com/ticstyle/DynDNS/actions/workflows/pipeline.yml)
[![HACS Validation](https://img.shields.io/github/actions/workflow/status/ticstyle/DynDNS/pipeline.yml?branch=main&label=HACS)](https://github.com/ticstyle/DynDNS/actions/workflows/pipeline.yml)
[![Ruff / Format](https://img.shields.io/github/actions/workflow/status/ticstyle/DynDNS/pipeline.yml?branch=main&label=Ruff%20%2F%20Format)](https://github.com/ticstyle/DynDNS/actions/workflows/pipeline.yml)
[![Mypy](https://img.shields.io/github/actions/workflow/status/ticstyle/DynDNS/pipeline.yml?branch=main&label=Mypy)](https://github.com/ticstyle/DynDNS/actions/workflows/pipeline.yml)
![Installs](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=Known%20installs&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.dyndns.total)

A lightweight Home Assistant custom integration designed to keep your public dynamic IP addresses up to date using any provider supporting the standard **DynDNS2** protocol.

### ✨ Features
* **Full UI Setup:** Configure your domain, credentials, and update server directly through the Home Assistant UI via Config Flow.
* **Native Reconfiguration:** Change your host credentials, server, or update parameters anytime using the integration cogwheel.
* **Live Update Interval:** Control the background update frequency (in minutes) dynamically via a `number` entity directly from dashboards or automations.
* **Manual Refresh Button:** Instantly force an IP update check on demand using the dedicated update button entity.
* **Diagnostic Sensors:** Track system health with a dedicated problem binary sensor and a UTC timestamp sensor recording the exact time of the last successful update.

To add this integration, please add the custom repository `https://github.com/ticstyle/DynDNS/` to HACS in your Home Assistant setup.

## 🚀 Installation

[![](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ticstyle&repository=DynDNS&category=Integration)

Via [HACS](https://hacs.xyz/) or manually copy the `dyndns` folder from the [latest release](https://github.com/ticstyle/DynDNS/releases/latest) to the `custom_components` folder inside your Home Assistant configuration directory.
