# DynDNS

<p align="center">
  <img src="https://raw.githubusercontent.com/ticstyle/DynDNS/main/custom_components/dyndns/brand/logo.png" alt="DynDNS Logo" width="800" />
</p>

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

A lightweight, powerful Home Assistant custom integration designed to keep your dynamic IP addresses updated using standard **DynDNS2** (Basic Auth) or **Custom HTTP GET** (Token Auth) protocols.

### ✨ Features
* **Multi-Protocol Support:** Switch seamlessly between standard **DynDNS2** (`/nic/update` with HTTP Basic Auth) and **Custom HTTP GET** (`/api/dyndns/update` with token authentication).
* **Full UI Setup & Reconfiguration:** Add domains, server addresses, credentials, and update intervals directly via Config Flow or reconfigure anytime using the integration cogwheel.
* **Live Update Interval Control:** Control background update frequencies in minutes live using a dedicated `number` entity without needing to restart.
* **Manual Refresh Button:** Force an instant IP update check on demand using the update button entity.
* **State Persistence:** Entities restore their last known state across Home Assistant restarts and integration reloads.
* **Diagnostic Sensors:** Track system health with a problem binary sensor and a UTC timestamp sensor recording the exact time of the last successful update.

To add this integration, please add the custom repository `https://github.com/ticstyle/DynDNS/` to HACS in your Home Assistant setup.

## 🚀 Installation

[![](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ticstyle&repository=DynDNS&category=Integration)

Via [HACS](https://hacs.xyz/) or manually copy the `dyndns` folder from the [latest release](https://github.com/ticstyle/DynDNS/releases/latest) to the `custom_components` folder inside your Home Assistant configuration directory.

## ⚙️ Configuration

[![](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=dyndns)

Add and adjust the integration via the Home Assistant User Interface.
