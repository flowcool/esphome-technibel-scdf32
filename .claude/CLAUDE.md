# ESPHome Technibel SCDF32

IR control for Technibel SCDF32 AC unit via ESP32 + ESPHome external_component.

## Architecture

- **Repo** (`~/claude_project/esphome-technibel-scdf32`): dev, docs, version control
- **Live NAS** (`/volume1/docker/homeassistant/esphome/`): mounted into ESPHome container, compiles/flashes
- **No auto-sync** — manual `command cp -f` from repo → NAS before any deploy
- HA config: `/volume1/docker/homeassistant/homeassistant/packages/` (MQTT climate entities)

## Key files

| File | Role |
|---|---|
| `esphome/ir-technibel-clim.yaml` | Main ESPHome device config |
| `esphome/libraries/technibel_ir.h` | C++ IR protocol implementation |
| `esphome/ir-clim-sniffer.yaml` | IR receiver/sniffer config |
| `homeassistant/climate-technibel-ha.yaml` | HA-side MQTT climate + automations |

## Protocol docs

- `docs/protocol.md` — IR frame format, timing, command encoding
- `docs/control-strategies.md` — AC mode control via TSOP IR injection
- `docs/wiring.md` — hardware wiring (TSAL6400 + 2N2222 circuit)
- `docs/troubleshooting.md` — known issues and fixes

## Deploy checklist

1. Edit config in repo
2. Validate: `esphome config ir-technibel-clim.yaml` inside ESPHome container
3. Copy to NAS: `command cp -f` repo files → live folder
4. Compile + flash from ESPHome dashboard
