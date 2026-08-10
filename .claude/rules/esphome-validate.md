---
description: Validate ESPHome components before proposing config changes
paths:
  - "esphome/**/*.yaml"
  - "esphome/**/*.h"
---

# ESPHome validation rules

## No climate.template

ESPHome has NO `climate: platform: template`. The template platform exists for sensor, switch, cover, number, etc. — but not climate. The only native path for a custom IR climate is a `climate_ir`-based external_component (C++ class inheriting `ClimateIR`).

Never assume a platform exists by analogy with other component domains.

## Validate before deploy

Before telling the user a config change is ready:
- Run `esphome config <file>.yaml` inside the actual ESPHome container
- Confirm it compiles without errors
- Never skip this step — a broken config deployed to the live environment has broken the HA climate entity before

## Repo ≠ live

Editing files in this repository has zero effect on the running device. Deploy only after verifying the dedicated VM target, its current live paths, the transfer mechanism, and rollback. Historical NAS paths are obsolete.
