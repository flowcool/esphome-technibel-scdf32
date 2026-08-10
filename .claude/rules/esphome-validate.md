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
- Never skip this step — a broken config pushed to the live NAS folder has bricked the HA climate entity before

## Repo ≠ live

Editing files in this repo has zero effect on the running device. Changes must be manually copied to the NAS live folder (`/volume1/docker/homeassistant/esphome/`).
