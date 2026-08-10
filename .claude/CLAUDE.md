# ESPHome Technibel SCDF32

IR control for Technibel SCDF32 AC unit via ESP32 + ESPHome external_component.

## Architecture

- **Repo** (`~/claude_project/esphome-technibel-scdf32`): dev, docs, version control
- **Live VM**: dedicated ESPHome and Home Assistant runtime, separate from this repository
- **No assumed auto-sync** — verify VM access, live paths, deployment method, and rollback before deploy
- Historical NAS paths are obsolete and must not be reused

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
2. Validate the repository configuration in an appropriate ESPHome environment
3. Review `git diff --numstat` and the semantic diff, then commit all intended project changes
4. Verify the dedicated VM target, live paths, deployment method, and rollback
5. Transfer the committed files explicitly and verify the live copy
6. Compile and flash from the live ESPHome environment

Never leave intended project changes only in the working tree at handoff. Report repository, remote, and live VM state separately.
